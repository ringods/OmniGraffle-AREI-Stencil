import glob
import os
# import plistlib
# import re
import shutil
import sys
# from argparse import ArgumentParser, Namespace
# from collections import defaultdict
from itertools import filterfalse
from typing import List, Dict, Any, Tuple

import cairosvg

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
svg_source_dir = os.path.join(current_dir, 'SVG')
svg_target_dir = os.path.join(current_dir, 'SVG-Resized')

def main():
    create_output_dir(svg_target_dir)

    for dirpath, dirnames, filenames in os.walk(svg_source_dir):
        target_dir = os.path.join(svg_target_dir, os.path.relpath(dirpath, svg_source_dir))
        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)
        for image in filenames:
            print(f'Processing {image}')
            cairosvg.svg2svg(url=os.path.join(dirpath, image), write_to=os.path.join(target_dir, image), scale=5)

    print('Images resized')


def create_output_dir(dir_name) -> None:
    shutil.rmtree(dir_name, ignore_errors=True)
    os.mkdir(dir_name)


def list_images(dir_path: str, name_includes: List[str], name_excludes: List[str]) -> List[str]:
    files = [f for f in glob.glob(os.path.join(dir_path, '**/*.svg'), recursive=True)]

    files = filter_file_name_include(files, name_includes)
    files = filter_file_name_exclude(files, name_excludes)

    files.sort()

    return files


def filter_file_name_include(files: List[str], keywords: List[str]) -> List[str]:
    if not keywords:
        return files

    return list(
        filter(lambda file: all(keyword in os.path.basename(file) for keyword in keywords), files)
    )


def filter_file_name_exclude(files: List[str], keywords: List[str]) -> List[str]:
    if not keywords:
        return files

    return list(
        filterfalse(lambda file: any(keyword in os.path.basename(file) for keyword in keywords), files)
    )

def get_destination_from_source(source:str) -> str:
    return source