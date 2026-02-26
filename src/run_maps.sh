#!/bin/bash

for file in /data/Twitter\ dataset/geoTwitter20-*.zip; do
    nohup python map.py --input_path "$file" --output_folder ../outputs &
done
