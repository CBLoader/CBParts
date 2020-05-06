import ast
import base64
import glob
import hashlib
import subprocess
import os
from typing import List, Set

import attr
from lxml import etree

BASEURL = 'https://cbloader.vorpald20.com/'
indexes = []
parts = []
indexed = set()

preview = etree.XSLT(etree.parse('D20Rules.xslt'))

@attr.s(auto_attribs=True, hash=False, eq=False)
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
        return f'<p>[{self.category}]: <a href="{self.url}" download="{self.name}" >{self.name}</a>' + (f'<br/> {self.desc}</p>' if self.desc else '</p>')

    def __hash__(self):
        return self.name.__hash__()

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.path == other.path
        elif isinstance(other, str):
            if self.name == other or self.path == other:
                return True
        return False

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.name < other.name

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

def MakeUpdateInfo(dir: str, part: str):
    path = os.path.join(dir, part)
    update_info = etree.Element('UpdateInfo')
    cid = subprocess.check_output(['git', 'rev-list', '-1', 'HEAD', path])
    ver = etree.SubElement(update_info, 'Version')
    ver.text = cid
    fname = etree.SubElement(update_info, 'Filename')
    fname.text = part
    return update_info


def patch_part(dir: str, part: str) -> None:
    path = os.path.join(dir, part)
    xml = etree.parse(path)
    update_info = xml.find('UpdateInfo')
    if update_info is None:
        if xml.find('Obsolete') is None:
            print(f'WARNING: {dir}/{part} has no UpdateInfo')
            update_info = MakeUpdateInfo(dir, part)
            xml.getroot().insert(0, update_info)
        else:
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
    preview(xml).write(os.path.splitext(path)[0] + '.html')
    if part.endswith('.index'):
        contents = []
        for p in xml.findall('Part'):
            fn = p.find('Filename')
            if fn is not None:
                indexed.add(fn.text)
                contents.append(fn.text)
        if not desc_text:
            desc_text ='<i>' + ', '.join(contents) + '</i>'
    return Info(part, os.path.join(dir, part), update_info.base, desc_text, pinned, category, version_hash(path), update_info.find('Version').text)

def version_hash(path: str) -> str:
    with open(path, encoding='utf-8') as f:
        h = hashlib.sha256(f.read().encode('utf-8'))
    return base64.b64encode(h.digest()).decode('utf-8')

def write_index() -> None:
    idxs = list(indexes)
    unindexed = set(parts) - indexed
    idxs.extend(unindexed)
    html = []
    with open('head.html') as f:
        html.append(f.read())
    doc = etree.Element("Indexes")
    def add(info: Info) -> None:
        tag = os.path.splitext(info.name)[1].strip('.').title()
        entry = etree.Element(tag, name=info.name, url=info.url, category=info.category, description=info.desc)
        entry.text = str(info)
        if info.pinned:
            doc.insert(0, entry)
            html.insert(1, info.html())
        else:
            doc.append(entry)
            html.append(info.html())

    for i in [i for i in idxs if i.pinned]:
        add(i)
    cats = set()
    for i in idxs:
        cats.add(i.category)
    categories = list(cats)
    categories.sort()
    for c in categories:
        incat = [i for i in idxs if i.category == c and not i.pinned]
        incat.sort()
        for i in incat:
            add(i)
    for i in unindexed:
        print(f'{i.name} is not indexed')

    tree = etree.ElementTree(doc)
    tree.write('index.xml', pretty_print=True)
    try:
        subprocess.run('zip', '-r', 'indexes.zip', 'indexes')
        html.append('<p><a href="indexes.zip">Download all indexes</a></p>')
    except Exception as c:
        print(c)
    html.append('</body></html>')
    with open('index.html', 'w') as f:
        f.writelines(html)

def checkForDups(listOfElems) -> Set[str]:
    ''' Check if given list contains any duplicates '''
    setOfElems = set()
    setOfDups = set()
    for elem in listOfElems:
        if elem in setOfElems:
            print(f'WARNING: Duplicate {elem} found in names')
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
        f.write('CBLoader Version File v2\n')
        for p in infos:
            if p.name not in dups:
                f.write(f'{p.name}:{p.parthash}:{p.version}\n')
            else:
                print(f'WARNING: Not writing V2 about duplicated {p.name}')

for v in os.walk('.'):
    do_folder(*v)
write_index()
writeV2()
