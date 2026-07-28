#!/usr/bin/env python3
import sys

current_store = None
total_sales = 0.0

for line in sys.stdin:
    data = line.strip().split("\t")
    if len(data) != 2:
        continue

    store, cost = data
    try:
        cost = float(cost)
    except ValueError:
        continue

    if current_store == store:
        total_sales += cost
    else:
        if current_store:
            print(f"{current_store}\t{total_sales:.2f}")
        current_store = store
        total_sales = cost

if current_store:
    print(f"{current_store}\t{total_sales:.2f}")