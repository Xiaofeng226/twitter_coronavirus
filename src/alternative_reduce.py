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
import matplotlib.ticker as ticker

# month number -> abbreviated name
MONTH_NAMES = {
    '01': 'Jan', '02': 'Feb', '03': 'Mar', '04': 'Apr',
    '05': 'May', '06': 'Jun', '07': 'Jul', '08': 'Aug',
    '09': 'Sep', '10': 'Oct', '11': 'Nov', '12': 'Dec'
}

# scan through all input files and construct dataset:
# counts[hashtag][day] = total tweets, where day is "MM-DD"
counts = defaultdict(lambda: defaultdict(int))

for path in args.input_paths:
    # extract month and day from filename e.g. "geoTwitter20-02-16.zip.lang" -> "02-16"
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

# build x-axis tick positions at the first day of each new month
tick_positions = []
tick_labels = []
seen_months = set()
for i, day in enumerate(all_days):
    month = day.split('-')[0]
    if month not in seen_months:
        tick_positions.append(i)
        tick_labels.append(MONTH_NAMES.get(month, month))
        seen_months.add(month)

# plot one line per hashtag using integer positions so ticks align cleanly
fig, ax = plt.subplots(figsize=(14, 6))

for hashtag in args.hashtags:
    y_values = [counts[hashtag].get(day, 0) for day in all_days]
    ax.plot(range(len(all_days)), y_values, marker='o', markersize=3, linewidth=1.5, label=hashtag)

ax.set_xticks(tick_positions)
ax.set_xticklabels(tick_labels)
ax.set_xlabel('Month')
ax.set_ylabel('Number of Tweets')
ax.set_title('Daily Tweet Counts by Hashtag (2020)')
ax.legend()
plt.tight_layout()
plt.savefig('hashtag_trends.png')
print('Plot saved to hashtag_trends.png')

