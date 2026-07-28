#!/usr/bin/env python3
import sys

current_key = None
total_co = 0.0
total_o3 = 0.0
count = 0

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) != 4:
        continue

    key, co, o3, temp = data
    try:
        co = float(co)
        o3 = float(o3)
    except ValueError:
        continue

    if current_key == key:
        total_co += co
        total_o3 += o3
        count += 1
    else:
        if current_key:
            city, month = current_key.split("_")
            print(f"{city}\tMois:{month}\tTotal_CO:{total_co:.2f}\tMoyenne_O3:{(total_o3/count):.2f}")
        current_key = key
        total_co = co
        total_o3 = o3
        count = 1

if current_key:
    city, month = current_key.split("_")
    print(f"{city}\tMois:{month}\tTotal_CO:{total_co:.2f}\tMoyenne_O3:{(total_o3/count):.2f}")