import ast
import base64
import glob
import hashlib
import os
from typing import List, Set

import attr
from lxml import etree

BASEURL = 'https://cbloader.vorpald20.com/'
indexes = []
parts = []


@attr.s(auto_attribs=True)
class Info():
    name: str
    path: str
    url: str
    desc: str
    pinned: bool
    category: str
    parthash: str
    version: str

    def __str__(self) -> str:
        return f'{self.category}: {self.url}' + f' ({self.desc})' if self.desc else ''
    
    def html(self) -> str:
        return f'<p>[{self.category}]: <a href="{self.url}">{self.name}</a>' + (f'<br/> {self.desc}</p>' if self.desc else '</p>')

def do_folder(dir: str, subs: List[str], files: List[str]) -> None:
    for part in [p for p in files if os.path.splitext(p)[1].lower() == '.part']:
        info = patch_part(dir, part)
        if info is not None:
            parts.append(info)
    for index in [p for p in files if os.path.splitext(p)[1].lower() == '.index']:
        info = patch_part(dir, index)
        if info is not None:
            indexes.append(info)

def SetOrCreate(update_info: etree.Element, elemName: str, text: str) -> None:
    sub = update_info.find(elemName)
    if sub is not None:
        sub.text = text
    else:
        etree.SubElement(update_info, elemName).text = text


def patch_part(dir: str, part: str) -> None:
    path = os.path.join(dir, part)
    xml = etree.parse(path)
    update_info = xml.find('UpdateInfo')
    if update_info is None:
        print(f'WARNING: {dir}/{part} has no UpdateInfo')
        return
    txt = os.path.splitext(path)[0] + '.txt'
    with open(txt, 'w') as f:
        f.write(update_info.find('Version').text)
    
    url = (BASEURL + update_info.base).replace('/./', '/')
    version_url = os.path.splitext(url)[0] + '.txt'
    SetOrCreate(update_info, 'PartAddress', url)
    SetOrCreate(update_info, 'VersionAddress', version_url)
    SetOrCreate(update_info, 'V2Address', BASEURL + 'versions2.txt')

    xml.write(path, pretty_print=True, xml_declaration=True, encoding='utf-8')
    description = update_info.find('Description')
    if description is not None:
        desc_text = description.text
        pinned = ast.literal_eval(description.get('pin', 'False'))
        category = description.get('category', None)
    else:
        desc_text = ''
        pinned = False
        category = None
    if category is None:
        if part.endswith('.part'):
            category = os.path.dirname(path)
        else:
            pelem = xml.find('Part')
            if pelem is None:
                return None
            address = pelem.find('PartAddress').text
            category = os.path.dirname(address)
        category = os.path.basename(category)
    return Info(part, os.path.join(dir, part), update_info.base, desc_text, pinned, category, version_hash(path), update_info.find('Version').text)

def version_hash(path: str) -> str:
    with open(path, encoding='utf-8') as f:
        h = hashlib.sha256(f.read().encode('utf-8'))
    return base64.b64encode(h.digest()).decode('utf-8')

def write_index() -> None:
    idxs = list(indexes)
    html = ['<html><body>']
    doc = etree.Element("Indexes")
    def add(info: Info) -> None:
        entry = etree.Element('Index', name=info.name, url=info.url, category=info.category, description=info.desc)
        entry.text = str(info)
        if info.pinned:
            doc.insert(0, entry)
            html.insert(1, info.html())
        else:
            doc.append(entry)
            html.append(info.html())
        idxs.remove(info)

    for i in [i for i in idxs if i.pinned]:
        add(i)
    cats = set()
    for i in idxs:
        cats.add(i.category)
    categories = list(cats)
    categories.sort()
    for c in categories:
        for i in [i for i in idxs if i.category == c]:
            add(i)
    
    tree = etree.ElementTree(doc)
    tree.write('index.xml', pretty_print=True)
    html.append('</body></html>')
    with open('index.html', 'w') as f:
        f.writelines(html)

def checkForDups(listOfElems) -> Set[str]:
    ''' Check if given list contains any duplicates '''    
    setOfElems = set()
    setOfDups = set()
    for elem in listOfElems:
        if elem in setOfElems:
            print(f'Duplicate {elem} found in names')
            setOfDups.add(elem)
        else:
            setOfElems.add(elem)         
    return setOfDups

def writeV2() -> None:
    infos = list(indexes)
    infos.extend(parts)
    names = [p.name for p in infos]
    dups = checkForDups(names)
    with open('versions2.txt', 'w') as f:
        for p in infos:
            if p.name not in dups:
                f.write(f'{p.name}:{p.parthash}:{p.version}\n')
            else:
                print(f'Not writing V2 about duplicated {p.name}')
            


for v in os.walk('.'):
    do_folder(*v)
write_index()
writeV2()
