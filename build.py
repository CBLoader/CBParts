import glob
from lxml import etree
import os
from typing import List

BASEURL = 'https://cbloader.vorpald20.com/'

def do_folder(dir: str, subs: List[str], files: List[str]) -> None:
    print(dir)
    for part in [p for p in files if os.path.splitext(p)[1].lower() == '.part']:
        print(part)
        patch_part(dir, part)
    print('---')

def patch_part(dir: str, part: str) -> None:
    xml = etree.parse(os.path.join(dir, part))
    update_info = xml.find('UpdateInfo')
    if update_info is None:
        print(f'WARNING: {dir}/{part} has no UpdateInfo')
        return
    txt = os.path.splitext(os.path.join(dir, part))[0] + '.txt'
    with open(txt, 'w') as f:
        f.write(update_info.find('Version').text)
    


for v in os.walk('.'):
    do_folder(*v)

