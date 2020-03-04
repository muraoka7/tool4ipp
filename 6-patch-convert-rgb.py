#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright 2020 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import glob
import multiprocessing as mp
import os
import sys

import numpy as np
from PIL import Image, ImageFile


ImageFile.LOAD_TRUNCATED_IMAGES = True


def process(f):
    print("Processing ... ", f)
    jpegs = glob.glob(os.path.join(f, "*.jpeg"))
    for j in jpegs:
        img = Image.open(j)
        if len(np.array(img).shape) != 3:
            img = img.convert("RGB")
            img.save(j)


files = glob.glob(os.path.join(sys.argv[1], "*"))

with mp.Pool(8) as p:
    p.map(process, files)


