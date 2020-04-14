import glob
from lxml import etree
import os
from typing import List

BASEURL = 'https://cbloader.vorpald20.com/'

def do_folder(dir: str, subs: List[str], files: List[str]) -> None:
    for part in [p for p in files if os.path.splitext(p)[1].lower() == '.part']:
        patch_part(dir, part)
    for index in [p for p in files if os.path.splitext(p)[1].lower() == '.index']:
        patch_part(dir, index)

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


for v in os.walk('.'):
    do_folder(*v)

