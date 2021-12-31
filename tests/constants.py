#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Constants for test cases.
"""
import pathlib


CURDIR = pathlib.Path(__file__).parent

OK_DATA_FILES = sorted((CURDIR / 'res').glob('ok/*.fit'))
NG_DATA_FILES = sorted((CURDIR / 'res').glob('ng/*.fit'))
