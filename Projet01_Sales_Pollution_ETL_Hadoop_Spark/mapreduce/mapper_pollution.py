#!/usr/bin/env python3

import sys

for line in sys.stdin:
    if line.startswith("Ville"):
        continue

    data = line.strip().split('\t')
    if len(data) == 6 :
        city,month,year,co,o3,temp = data
        print(f"{city}_{month}\t{co}\t{o3}\t{temp}")