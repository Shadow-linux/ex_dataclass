import json
import os

import sys

from src import m
from time import perf_counter as pc
from collections import deque

b_file_10000 = "benchmark/basic_10000.json"

with open(b_file_10000) as fd:
    data_1 = fd.read()

test_data = json.loads(data_1)
real_test_data = []
que_test_data = deque()
for _ in range (0 , 1000):
    for item in test_data['data']:

        real_test_data.append(item)
        que_test_data.append(item)

print(len(real_test_data))

def TestBench(data, is_print_data=False):
    start = pc()
    count = 0
    tmp_list = []
    for item in data:
        count += 1
        tmp_list.append(item)
    print(f'list: {pc() - start}')


def TestBenchWithDeque(data, is_print_data=False):
    start = pc()
    count = 0
    tmp_deque = deque()
    for item in data:
        count += 1
        tmp_deque.append(item)
    print(f'deque: {pc() - start}')


for _ in range(0, 10):
    TestBenchWithDeque(que_test_data)

for _ in range(0, 10):
    TestBench(real_test_data)
