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

import json
import multiprocessing as mp
import os
from pathlib import Path
import sys


p = Path(sys.argv[1])
art_dirs = list(p.glob("*"))


def check_section_num(doc):
    sections = doc["sections"]
    return 10 <= len(sections) <= 50


def check_image_num(doc):
    return len(doc["images"]) >= 2


def check_image(doc, art_dir):
    ids = [i["id"] for i in doc["images"]]
    return all([os.path.exists(os.path.join(art_dir, "{}.jpeg".format(i))) for i in ids])


def check_image_has_caption(doc):
    return all([i["caption"]  != "" for i in doc["images"]])


def check_article_name(doc):
    if doc["title"].startswith("List of") or doc["title"].startswith("Lists"):
        return False
    else:
        return True


def validate(art_dir):
    doc = json.loads(open(os.path.join(art_dir, "doc.json")).read())
    if not check_section_num(doc):
        print("NG Section num", art_dir)
        return str(art_dir)
    if not check_image_num(doc):
        print("NG Image num", art_dir)
        return str(art_dir)
    if not check_image(doc, art_dir):
        print("NG Image missing", art_dir)
        return str(art_dir)
    if not check_image_has_caption(doc):
        print("NG Image caption missing", art_dir)
        return str(art_dir)
    if not check_article_name(doc):
        print("NG article name", art_dir)
        return str(art_dir)

    print("OK", art_dir)


with mp.Pool(8) as p:
    res = p.map(validate, art_dirs)

with open("7-failed.txt", "w") as f:
    for r in res:
        if r is not None:
            f.write(r + "\n")
