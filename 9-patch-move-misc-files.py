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


p = Path(sys.argv[1])

files = list(p.glob("*/*.license"))
files += list(p.glob("*/removed.json"))


def move_to_info(f):
    dirname = os.path.join(os.path.dirname(f), "info")
    os.makedirs(dirname, exist_ok=True)
    basename = os.path.basename(f)
    t = os.path.join(dirname, basename)
    os.rename(f, t)


with mp.Pool(8) as p:
    res = p.map(move_to_info, files)
