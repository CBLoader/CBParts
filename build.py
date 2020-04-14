import ast
import glob
from lxml import etree
import os
from typing import List

BASEURL = 'https://cbloader.vorpald20.com/'
indexes = []

def do_folder(dir: str, subs: List[str], files: List[str]) -> None:
    for part in [p for p in files if os.path.splitext(p)[1].lower() == '.part']:
        patch_part(dir, part)
    for index in [p for p in files if os.path.splitext(p)[1].lower() == '.index']:
        info = patch_part(dir, index)
        if info:
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
    return (part, os.path.join(dir, part), update_info.base, desc_text, pinned, category)

def write_index() -> None:
    doc = etree.Element("Indexes")
    for (name, _, url, desc, pinned, category) in indexes:
        entry = etree.Element('Index', name=name, url=url, category=category)
        entry.text = desc
        if pinned:
            doc.insert(0, entry)
        else:
            doc.append(entry)
    tree = etree.ElementTree(doc)
    tree.write('index.xml', pretty_print=True)

for v in os.walk('.'):
    do_folder(*v)
    write_index()

