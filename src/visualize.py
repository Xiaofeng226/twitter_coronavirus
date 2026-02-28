#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)  
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'NanumGothic'
# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the count values
items = sorted(counts[args.key].items(), key=lambda item: (item[1],item[0]), reverse=True)
for k,v in items:
    print(k,':',v)

top10 = items[:10]
top10_sorted = sorted(top10, key=lambda item: item[1])
keys = [item[0] for item in top10_sorted]
values = [item[1] for item in top10_sorted]

plt.figure(figsize=(12, 6))
plt.bar(keys, values)
plt.xlabel('Language Keys')
plt.ylabel('Number of Tweets')
plt.title(f'{args.key} by {os.path.basename(args.input_path)}')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

input_name = os.path.basename(args.input_path)
output_path = f'{input_name}.png'
plt.savefig(output_path)
print(f'saved to {output_path}')
