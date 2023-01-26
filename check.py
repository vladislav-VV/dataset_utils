#!/bin/env python3

import os
import sys
import datetime
from tqdm import tqdm


class Log:

    def __init__(self, fname):
        self.fname = fname
        self.data = []

    def save(self, print_summary=False):
        if print_summary:
            print("for {} found {} files".format(self.fname, len(self.data)))
        with open(self.fname, "wt") as f:
            for line in self.data:
                f.write(line + "\n")

    def append(self, data):
        self.data.append(data)



fname = r'E:\codepy\UTILS\generate-list-path_im-train\train.txt'
cache_period = 1000

if len(sys.argv) > 1:
    fname = sys.argv[1]

if not os.path.exists(fname):
    print("list file {} not exist".format(fname))
    exit(0)

fname_cache = os.path.split(fname)[1] + '.cache'
if os.path.exists(fname_cache):
    fname = fname_cache

with open(fname, 'rt') as f:
    image_list = f.read().splitlines()

now = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

warning_log = Log("warning_list_{}.txt".format(now))
noexist_log = Log("noexist_list_{}.txt".format(now))

progress = tqdm(total=len(image_list))

for n, image_path in enumerate(image_list):

    progress.update()

    if n % cache_period == 0:
        warning_log.save()
        noexist_log.save()
        with open(fname_cache, "wt") as f:
            for name in image_list[n:-1]:
                f.write(name + "\n")

    if not os.path.exists(image_path):
        print("image file {} not exist".format(image_path))
        noexist_log.append(image_path)
        continue

    labels_path = os.path.splitext(image_path)[0] + '.txt'
    if not os.path.exists(labels_path):
        print("labels file {} not exist".format(labels_path))
        noexist_log.append(labels_path)
        continue

    with open(labels_path, 'rt') as f:
        labels_list = f.read().splitlines()

    labels_set = set(labels_list) 

    if len(labels_set) == len(labels_list):
        continue

    warning_log.append(labels_path)

    os.rename(labels_path, labels_path + '.backup')

    with open(labels_path, "wt") as f:
        for line in labels_set:
            f.write(line + "\n")
        
    print("image name = ", image_path)
    print("labels name = ", labels_path)
    print("labels list = \n", labels_list)
    print("labels set = \n", labels_set)

warning_log.save(True)
noexist_log.save(True)