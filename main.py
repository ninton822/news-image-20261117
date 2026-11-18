#!/usr/bin/env python3
"""Entry program for news-image-20261117 (Python 3.13, standard library only).

Copies the committed entry.png to /output/entry.png, byte for byte.
The image itself is the entry: a newspaper front page summing up Tuesday
17 November 2026, drawn with PIL by render.py and committed as entry.png.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    # The program runs twice and both runs must write the same bytes:
    # a plain byte copy is deterministic by construction.
    assert os.path.getsize(src) == os.path.getsize(dst)


if __name__ == "__main__":
    main()
