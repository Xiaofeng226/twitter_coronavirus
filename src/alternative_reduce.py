#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths', nargs='+', required=True)
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

# imports
import os
import json
from collections import defaultdict
import matplotlib
matplotlib.rcParams['font.family'] = 'Baekmuk Dotum'
import matplotlib.pyplot as plt

# month number -> abbreviated name
MONTH_NAMES = {
    '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
    '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
    '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
}

# scan through all input files and construct dataset:
# counts[hashtag][month] = total tweets
counts = defaultdict(lambda: defaultdict(int))

for path in args.input_paths:
    # extract month from filename e.g. "geoTwitter20-02-16.zip.lang" -> "02"
    basename = os.path.basename(path)
    parts = basename.split('-')
    if len(parts) >= 3:
        month = parts[1]
    else:
        month = 'unknown'

    with open(path) as f:
        tmp = json.load(f)

    for hashtag in args.hashtags:
        if hashtag in tmp:
            counts[hashtag][month] += sum(tmp[hashtag].values())

# collect all months sorted chronologically
all_months = sorted(set(
    month for hashtag in args.hashtags for month in counts[hashtag]
))

month_labels = [MONTH_NAMES.get(m, m) for m in all_months]

# plot one line per hashtag
for hashtag in args.hashtags:
    y_values = [counts[hashtag].get(month, 0) for month in all_months]
    plt.plot(month_labels, y_values, marker='o', markersize=5, linewidth=2, label=hashtag)

plt.xlabel('Month')
plt.ylabel('Number of Tweets')
plt.title('Monthly Tweet Counts by Hashtag (2020)')
plt.legend()
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('hashtag_trends.png')
print('Plot saved to hashtag_trends.png')
