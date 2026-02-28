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

# scan through all input files and construct dataset:
# counts[hashtag][day] = total tweets
counts = defaultdict(lambda: defaultdict(int))

for path in args.input_paths:
    # extract day label from filename e.g. "geoTwitter20-02-16.zip.lang" -> "02-16"
    basename = os.path.basename(path)
    parts = basename.split('-')
    if len(parts) >= 3:
        month = parts[1]
        day = parts[2].split('.')[0]
        day_label = month + '-' + day
    else:
        day_label = basename

    with open(path) as f:
        tmp = json.load(f)

    for hashtag in args.hashtags:
        if hashtag in tmp:
            counts[hashtag][day_label] += sum(tmp[hashtag].values())

# collect all days sorted chronologically
all_days = sorted(set(
    day for hashtag in args.hashtags for day in counts[hashtag]
))

# plot one line per hashtag
for hashtag in args.hashtags:
    y_values = [counts[hashtag].get(day, 0) for day in all_days]
    plt.plot(all_days, y_values, marker='o', markersize=3, linewidth=1.5, label=hashtag)

plt.xlabel('Day of Year')
plt.ylabel('Number of Tweets')
plt.title('Daily Tweet Counts by Hashtag')
plt.legend()
plt.xticks(rotation=45, ha='right', fontsize=7)
plt.tight_layout()
plt.savefig('hashtag_trends.png')
print('Plot saved to hashtag_trends.png')
