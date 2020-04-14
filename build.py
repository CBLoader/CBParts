import ast
import glob
from lxml import etree
import os
from typing import List
import attr

BASEURL = 'https://cbloader.vorpald20.com/'
indexes = []


@attr.s(auto_attribs=True)
class Info():
    name: str
    path: str
    url: str
    desc: str
    pinned: bool
    category: str

    def __str__(self) -> str:
        return f'{self.category}: {self.url}' + f' ({self.desc})' if self.desc else ''
    
    def html(self) -> str:
        return f'<p>[{self.category}]: <a href="{self.url}">{self.name}</a>' + (f'<br/> {self.desc}</p>' if self.desc else '</p>')

def do_folder(dir: str, subs: List[str], files: List[str]) -> None:
    for part in [p for p in files if os.path.splitext(p)[1].lower() == '.part']:
        patch_part(dir, part)
    for index in [p for p in files if os.path.splitext(p)[1].lower() == '.index']:
        info = patch_part(dir, index)
        if info is not None:
            indexes.append(info)

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
    part_address = update_info.find('PartAddress')
    if part_address is not None:
        part_address.text = url
    else:
        etree.SubElement(update_info, 'PartAddress').text = url

    version_url = os.path.splitext(url)[0] + '.txt'
    version_address = update_info.find('VersionAddress')
    if version_address is not None:
        version_address.text = version_url
    else:
        etree.SubElement(update_info, "VersionAddress").text = version_url
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
    return Info(part, os.path.join(dir, part), update_info.base, desc_text, pinned, category)

def write_index() -> None:
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
        indexes.remove(info)

    for i in [i for i in indexes if i.pinned]:
        add(i)
    cats = set()
    for i in indexes:
        cats.add(i.category)
    categories = list(cats)
    categories.sort()
    for c in categories:
        for i in [i for i in indexes if i.category == c]:
            add(i)
    
    tree = etree.ElementTree(doc)
    tree.write('index.xml', pretty_print=True)
    html.append('</body></html>')
    with open('index.html', 'w') as f:
        f.writelines(html)
     

for v in os.walk('.'):
    do_folder(*v)
write_index()

