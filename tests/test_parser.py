#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>
# SPDX-License-Identifier: MIT
#
# pylint: disable=missing-docstring,invalid-name,too-few-public-methods
"""Test cases for FIT parser.
"""
import anyconfig
import anyconfig.ioinfo
import fitdecode
import pytest

import anyconfig_fit_backend as TT
import tests.constants


@pytest.mark.parametrize('in_path', tests.constants.NG_DATA_FILES)
def test_load_ng_data_files(in_path):
    # .. seealso:: fitdecode.exceptions
    exp_excs = (
        fitdecode.FitError,
        fitdecode.FitHeaderError,
        fitdecode.FitCRCError,
    )

    with pytest.raises(exp_excs):
        _ = TT.Parser().load(
            anyconfig.ioinfo.make(in_path), ac_ordered=True,
            check_crc=True
        )


@pytest.mark.parametrize('in_path', tests.constants.OK_DATA_FILES)
def test_load_ok_data_files(in_path, tmp_path):
    try:
        data = TT.Parser().load(
            anyconfig.ioinfo.make(in_path), ac_ordered=True
        )
        assert data
        assert isinstance(data, list)

        exp_path = str(in_path).replace('.fit', '.json')
        out_path = tmp_path / 'out.json'

        anyconfig.dump(data, out_path)
        odata = anyconfig.load(out_path, ac_ordered=False)
        exp = anyconfig.load(exp_path, ac_ordered=False)

        assert odata == exp, f'{odata!r} vs. {exp!r}'

    except AssertionError as exc:
        raise AssertionError(f'file: {in_path}, exc={exc!s}') from exc

# vim:sw=4:ts=4:et:
