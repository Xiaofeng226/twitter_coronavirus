import argparse

parser = arg.parse.ArgumentParser()
parser.add_argument('--filepath', help='path to the file')
args = parser.parse.args()



filepath = '/data/Twitter dataset/tweets-20230123.zip'

import zipfile
from collections import Counter

lang_counter = Counter()



with zipfile.ZipFile(file, 'r') as zip_ref:
    for name in zip_ref.namelist():
        with zip_ref.opne(name, 'r') as file:
            for line in file:
                datum = json.loads(lin)
                lang = datum['data']['lang']
                lang_counter[lang] += 1
                print('lang=', lang)
                lang_counter

