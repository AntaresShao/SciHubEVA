#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import platform
import subprocess

from pathlib import Path
from typing import List
from pdfminer.psparser import PSLiteral, PSKeyword


RANGE_QUERY_PATTERN = re.compile(r'\{\d+\-\d+\}')


def center_window(window, parent_window):
    parent_window_center_x = parent_window.x() + int(parent_window.width() / 2)
    parent_window_center_y = parent_window.y() + int(parent_window.height() / 2)

    window_x = parent_window_center_x - int(window.width() / 2)
    window_y = parent_window_center_y - int(window.height() / 2)

    window.setPosition(window_x, window_y)


def make_pdf_metadata_str(value) -> str:
    if isinstance(value, bytes):
        metadata_str = value.decode('utf-8')
    elif isinstance(value, str):
        metadata_str = value
    elif isinstance(value, (PSLiteral, PSKeyword)):
        metadata_str = make_pdf_metadata_str(value.name)
    else:
        metadata_str = ''

    return metadata_str


def pdf_metadata_moddate_to_year(moddate: str) -> str:
    if moddate.startswith('D:'):
        year = moddate[2:6]
    else:
        year = moddate[:4]

    return year


def open_file(file: str, timeout=3):
    if platform.system() == 'Darwin':
        subprocess.call(['open', file], timeout=timeout)
    elif platform.system() == 'Windows':
        os.startfile(file)
    else:
        subprocess.call(['xdg-open', file], timeout=timeout)


def open_directory(directory: str, timeout=3):
    if platform.system() == 'Darwin':
        subprocess.call(['open', directory], timeout=timeout)
    elif platform.system() == 'Windows':
        subprocess.call(['explorer', str(Path(directory))], timeout=timeout)
    else:
        subprocess.call(['xdg-open', directory], timeout=timeout)


def is_text_file(path: str) -> bool:
    try:
        with open(path, 'rt') as f:
            f.readlines()
    except:
        return False

    return True


def is_range_query(query: str) -> bool:
    if len(RANGE_QUERY_PATTERN.findall(query)) == 1:
        return True
    else:
        return False


def gen_range_query_list(query: str) -> List[str]:
    range_pattern = RANGE_QUERY_PATTERN.findall(query)[0]
    range_from_to = range_pattern.replace('{', '').replace('}', '').split('-')
    range_from = range_from_to[0]
    range_to = range_from_to[1]

    if len(range_from) == len(range_to):
        digit = len(range_from)
        range_item_pattern = '{:0>' + str(digit) + 'd}'
        range_items = [range_item_pattern.format(i) for i in range(int(range_from), int(range_to) + 1)]
    else:
        range_items = [str(i) for i in range(int(range_from), int(range_to) + 1)]

    return [query.replace(range_pattern, range_item) for range_item in range_items]


def is_windows():
    return platform.system() == 'Windows'


def is_macos():
    return platform.system() == 'Darwin'


def get_log_directory() -> Path:
    if is_macos():
        log_directory = Path.home() / 'Library/Logs/SciHubEVA'
    elif is_windows():
        log_directory = Path.home() / 'AppData/Local/SciHubEVA'
    else:
        log_directory = Path('/var/log/SciHubEVA')

    if not log_directory.exists():
        log_directory.mkdir()

    return log_directory


BASE_DIR = Path(os.path.dirname(__file__)) / '..'
CAPTCHA_MODEL_DIR = BASE_DIR / 'models'
IMAGES_DIR = BASE_DIR / 'images'
CONF_DIR = BASE_DIR / 'conf'
TRANSLATION_DIR = BASE_DIR / 'translations'
UI_DIR = BASE_DIR / 'ui'


__all__ = [
    'RANGE_QUERY_PATTERN',
    'center_window',
    'make_pdf_metadata_str',
    'pdf_metadata_moddate_to_year',
    'open_file',
    'open_directory',
    'is_text_file',
    'is_range_query',
    'gen_range_query_list',
    'get_log_directory',
    'is_windows',
    'is_macos',
    'BASE_DIR',
    'CAPTCHA_MODEL_DIR',
    'IMAGES_DIR',
    'CONF_DIR',
    'TRANSLATION_DIR',
    'UI_DIR'
]
