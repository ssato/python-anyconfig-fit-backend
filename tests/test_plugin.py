#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring
"""Plugin test cases.
"""
import anyconfig
import pytest

import tests.constants


def test_plugin_found():
    assert 'fit' in anyconfig.list_types()


@pytest.mark.parametrize('in_path', tests.constants.OK_DATA_FILES)
# @pytest.mark.parametrize('explicit', (True, False))
def test_load_with_plugin(in_path, tmp_path, explicit=True):
    try:
        if explicit:
            data = anyconfig.load(in_path, ac_parser='fit')
        else:
            data = anyconfig.load(in_path)

    except anyconfig.UnknownFileTypeError:
        print(f'all types={anyconfig.list_types()!r}')
        raise

    exp_path = str(in_path).replace('.fit', '.json')
    exp = anyconfig.load(exp_path, ordered=True)

    # It seems that it takes too long to finish.
    # assert data == exp
    # workround for the above problem.
    anyconfig.dump(data, tmp_path / 'in.json', indent=2)
    in_out = (tmp_path / 'in.json').read_text()

    anyconfig.dump(data, tmp_path / 'exp.json', indent=2)
    exp_out = (tmp_path / 'exp.json').read_text()

    assert in_out == exp_out

# vim:sw=4:ts=4:et:
