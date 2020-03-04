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

from glob import glob
import json
import multiprocessing as mp
import os
from pathlib import Path
import sys
from xml.etree import ElementTree as ET


p = Path(sys.argv[1])
art_dirs = list(p.glob("*"))


def exist(img_name, art_dir):
    files = glob(os.path.join(art_dir, f"*-{img_name}.license"))
    if len(files) == 0:
        return False
    img_file = os.path.basename(files[0]).split("-")[0] + ".jpeg"
    if os.path.exists(os.path.join(art_dir, img_file)):
        return True
    return False


def convert(art_dir):
    try:
        d1, artdirname = os.path.split(art_dir)
        if not os.path.exists(os.path.join(art_dir, "doc.org.xml")):  # remove later
            print(f"remove_pi.py may not be applied to '{art_dir}' yet.")
            return str(art_dir)                                       # remove later
        tree = ET.parse(os.path.join(art_dir, "doc.xml"))
        root = tree.getroot()
        doc_json = {"title": root.get("title"), "url": root.get("url")}
        section_nodes = []
        image_nodes = []
        # In doc.json, section id is reindexed instead of using the original id
        for sidx, section in enumerate(root):
            # If text of section appears after <image> tag(s), `section.text` does not have it.
            # workaround: Concatenate all text by `itertext()`, then, remove all the image captions from them.
            alltext = " ".join([t.strip().replace("\n", "") for t in section.itertext()])
            for iidx, img in enumerate(section):
                caption = img.text.strip().replace("\n", " ")
                alltext = alltext.replace(caption, "")
                if img.get("name").split(".")[-1] not in ["jpg", "jpeg", "JPG", "JPEG", "png", "PNG"]:
                    continue
                if exist(img.get("name"), art_dir):
                    image_nodes.append({"id": int(img.get("id")),
                                        "caption": caption,
                                        "section": sidx,
                                        "filepath": os.path.join(artdirname, img.get("id") + ".jpeg")})
            section_nodes.append({"id": sidx, "title": section.get("title"), "text": alltext.strip()})

        doc_json["sections"] = section_nodes
        doc_json["images"] = image_nodes

        with open(os.path.join(art_dir, "doc.json"), "w") as f:
            json.dump(doc_json, f, ensure_ascii=False, indent=4)
    except:
        import traceback
        traceback.print_exc()
        return str(art_dir)


with mp.Pool(8) as p:
    res = p.map(convert, art_dirs)

with open("4-failed.txt", "w") as f:
    for r in res:
        if r is not None:
            f.write(r + "\n")
