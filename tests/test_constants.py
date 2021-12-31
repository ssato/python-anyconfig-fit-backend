#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
"""Test cases for .constants.
"""
import tests.constants as TT


def test_data_files_exist():
    assert TT.OK_DATA_FILES, "No OK data files were found!"
    assert TT.NG_DATA_FILES, "No NG data files were found!"
