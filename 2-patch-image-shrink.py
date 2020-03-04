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

import multiprocessing as mp
import os
from pathlib import Path
import sys

from PIL import Image


p = Path(sys.argv[1])
image_files = list(p.glob("*/*.jpeg"))


def shrink(image_file):
    try:
        size = os.stat(image_file).st_size
        if size < 100000:
            return
        elif size > 1000000:  # 1MB
            quality = 5
        elif size > 500000: # 500kb
            quality = 10
        else:
            quality = 15
        img = Image.open(image_file)
        img = img.convert("RGB")
        img.save(str(image_file), quality=quality)
        size_after = os.stat(image_file).st_size
        print("Convert {} from {} to {} (quality={})".format(image_file, size, size_after, quality))
    except:
        import traceback
        traceback.print_exc()
        return image_file


with mp.Pool(12) as p:
    res = p.map(shrink, image_files)


with open("2-failed.txt", "w") as f:
    for r in res:
        if r is not None:
            f.write(str(r) + "\n")


