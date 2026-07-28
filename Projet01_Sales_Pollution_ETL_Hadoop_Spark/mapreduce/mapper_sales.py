#!/usr/bin/env python3

import sys

for line in sys.stdin :

    data = line.strip().split('\t')
    if len(data) == 6:
        _,_,store,_,cost,_= data
        print(f"{store}\t{cost}")