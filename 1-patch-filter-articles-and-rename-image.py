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
import re
import sys
import traceback

from bs4 import BeautifulSoup
from PIL import Image

from download_images import get_license_info, is_ok


p = Path(sys.argv[1])
art_dirs = list(p.glob("*"))


def file_paths(article_path):
    return list([i for i in article_path.glob("*-File:*") if not str(i).endswith(".soup") and not str(i).endswith(".license")])


def have_file_names(article_path):
    images = file_paths(article_path)
    return set([re.sub(r"^[0-9]*-", "", str(i).split("/")[-1]) for i in images]), images


def should_have_file_names(article_path):
    jsonf = list(article_path.glob("meta.json"))[0]
    return set(json.load(open(jsonf))["image_filenames"])


def have_all_images(have_files, should_have_files):
    return len(have_files.difference(should_have_files)) == 0


def have_enough_images(should_have_files, allowed_extensions=set(["jpg", "JPG", "jpeg","JPEG", "png", "PNG", ]), th=2):
    targeted = [f for f in should_have_files if f.split(".")[-1] in allowed_extensions]
    return len(targeted) >= th


def is_targeted(filename):
    if filename.split(".")[-1] in ["jpg", "JPG", "jpeg", "JPEG", "png", "PNG"]:
        return True
    else:
        return False


def is_licensed(img_file):
    li_file = img_file + ".license"
    if os.path.isfile(li_file):
        return is_ok(open(li_file).read())
    else:
        soup_file = img_file + ".soup"
        if not os.path.isfile(soup_file):
            return False
        soup = BeautifulSoup(open(soup_file).read(), "lxml")
        license = get_license_info(soup)
        with open(li_file, "w") as fo:
            fo.write(license + "\n")
        return is_ok(license)


def check(article_path):
    print("Process ... ", article_path)
    try:
        should_have_files = should_have_file_names(article_path)
        isok = have_enough_images(should_have_files)
        if not isok:
            print(f"Not enough image: {article_path}")
            return str(article_path)

        have_files, have_files_full_path = have_file_names(article_path)
        for hf in have_files_full_path:
            hf = str(hf)
            if is_targeted(hf) and is_licensed(hf):
                # rename image file name by leaving only the image id
                # E.g. 1-File:Apple.jpg -> 1.jpeg
                new_name = re.sub(r"-File:.*", ".jpeg", hf)
                os.rename(str(hf), new_name)
                Image.open(new_name)
            else:
                os.remove(hf)
                os.remove(hf + ".license")
    except:
        traceback.print_exc()
        return str(article_path)


with mp.Pool(8) as p:
    res = p.map(check, art_dirs)


with open("1-failed.txt", "w") as f:
    for r in res:
        if r is not None:
            f.write(r + "\n")
