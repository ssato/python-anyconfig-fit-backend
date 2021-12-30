#
# Copyright (C) 2021 Satoru SATOH <satoru.satoh@gmail.com>.
# SPDX-License-Identifier: MIT
#
r"""Very experimental loader parse FIT data files based on
fitdecode.cmd.fitjson.

- Format to support: FIT data files
- Requirements: fitdecode
- Development Status :: 4 - Beta
- Limitations:

  - Load function only and it doesn't support dump function
  - It should have some limitations I'm not aware of

Chnagelog:

    .. versionadded:: 0.1.0
"""
import collections
import datetime
import typing

import anyconfig.backend.base
import fitdecode

if typing.TYPE_CHECKING:
    import types

    DataDictT = typing.OrderedDict[str, typing.Any]

    FitFrame = typing.Union[
        types.GeneratorType,
        fitdecode.FitChunk,
        datetime.time,
        datetime.datetime,
        fitdecode.FitChunk,
        fitdecode.types.FieldDefinition,
        fitdecode.types.DevFieldDefinition,
        fitdecode.types.FieldData,
        fitdecode.FitHeader,
        fitdecode.FitCRC,
        fitdecode.FitDefinitionMessage,
        fitdecode.FitDataMessage
    ]

    DataItemT = typing.Tuple[str, typing.Any]


def items_to_datadict(*items: 'DataItemT') -> 'DataDictT':
    """Utility to make a data dict from given ``items``."""
    return collections.OrderedDict(items)


def from_datetime_or_time(
    obj: typing.Union[datetime.datetime, datetime.time]
) -> str:
    """Make a ISO 8601 format str represents given ``obj``."""
    return obj.isoformat()


def from_chunk(obj: fitdecode.FitChunk) -> 'DataDictT':
    """Make a dict object represents given FitChunk ``obj``.
    """
    return items_to_datadict(
        ('index', obj.index),    # int, > 0
        ('offset', obj.offset),  # do.
        ('size', len(obj.bytes))   # do.
    )


def from_field_def(obj: fitdecode.types.FieldDefinition) -> 'DataDictT':
    """Make a dict object represents given FieldDefinition ``obj``.
    """
    return items_to_datadict(
        ('name', obj.name),                      # str
        ('def_num', obj.def_num),                # int, > 0
        ('type_name', obj.type.name),            # str
        ('base_type_name', obj.base_type.name),  # str
        ('size', obj.size)                       # int, > 0
    )


def from_dev_field_def(
    obj: fitdecode.types.DevFieldDefinition
) -> 'DataDictT':
    """Make a dict object represents given DevFieldDefinition ``obj``.
    """
    return items_to_datadict(
        ('name', obj.name),
        ('dev_data_index', obj.dev_data_index),
        ('def_num', obj.def_num),
        ('type_name', obj.type.name),
        ('size', obj.size)
    )


TIME_DATA_NAMES: typing.FrozenSet[str] = frozenset((
    'timestamp',
    'time_created',
    'start_time',
))


def from_field_data(obj: fitdecode.types.FieldData) -> 'DataDictT':
    """Make a dict object represents given FieldData ``obj``.
    """
    if obj.name in TIME_DATA_NAMES:
        val = from_datetime_or_time(obj.value)
    else:
        val = obj.value

    return items_to_datadict(
        ('name', obj.name),
        ('value', val),
        ('units', obj.units if obj.units else ''),
        ('def_num', obj.def_num),
        ('raw_value', obj.raw_value)
    )


def from_header(obj: fitdecode.FitHeader) -> 'DataDictT':
    """Make a dict object represents given FitHeader ``obj``.
    """
    crc = obj.crc if obj.crc else 0

    return items_to_datadict(
        ('frame_type', 'header'),
        ('header_size', obj.header_size),
        ('proto_ver', obj.proto_ver),
        ('profile_ver', obj.profile_ver),
        ('body_size', obj.body_size),
        ('crc', f'{crc:#06x}'),
        ('crc_matched', obj.crc_matched),
        ('chunk', from_chunk(obj.chunk))  # FitChunk
    )


def from_crc(obj: fitdecode.FitCRC) -> 'DataDictT':
    """Make a dict object represents given FitCRC ``obj``.
    """
    return items_to_datadict(
        ('frame_type', 'crc'),
        ('crc', f'{obj.crc:#06x}'),
        ('matched', obj.matched),
        ('chunk', from_chunk(obj.chunk))  # FitChunk
    )


def from_def_message(obj: fitdecode.FitDefinitionMessage) -> 'DataDictT':
    """Make a dict object represents given FitDefinitionMessage ``obj``.
    """
    return items_to_datadict(
        ('frame_type', 'definition_message'),
        ('name', obj.name),
        (
            'header',
            items_to_datadict(
                ('local_mesg_num', obj.local_mesg_num),
                ('time_offset', obj.time_offset),
                ('is_developer_data', obj.is_developer_data),
            )
         ),
        ('global_mesg_num', obj.global_mesg_num),
        ('endian', obj.endian),
        (
            'field_defs',
            [from_field_def(d) for d in obj.field_defs]
         ),
        (
            'dev_field_defs',
            [from_dev_field_def(d) for d in obj.dev_field_defs]
         ),
        ('chunk', from_chunk(obj.chunk))
    )


def from_data_message(obj: fitdecode.FitDataMessage) -> 'DataDictT':
    """Make a dict object represents given FitDataMessage ``obj``.
    """
    return items_to_datadict(
        ('frame_type', 'data_message'),
        ('name', obj.name),
        (
            'header',
            items_to_datadict(
                ('local_mesg_num', obj.local_mesg_num),
                ('time_offset', obj.time_offset),
                ('is_developer_data', obj.is_developer_data),
            )
        ),
        (
            'fields',
            [from_field_data(f) for f in obj.fields]
         ),
        ('chunk', from_chunk(obj.chunk))
    )


# .. seealso:: fitdecode.cmd.fitjson.RecordJSONEncoder.default
RECORD_TO_ODICT_MAP: typing.Dict['FitFrame', typing.Callable] = {
    types.GeneratorType: list,
    datetime.time: from_datetime_or_time,
    datetime.datetime: from_datetime_or_time,
    fitdecode.FitChunk: from_chunk,
    fitdecode.types.FieldDefinition: from_field_def,
    fitdecode.types.DevFieldDefinition: from_dev_field_def,
    fitdecode.types.FieldData: from_field_data,
    fitdecode.FitHeader: from_header,
    fitdecode.FitCRC: from_crc,
    fitdecode.FitDefinitionMessage: from_def_message,
    fitdecode.FitDataMessage: from_data_message,
}

FRAME_TYPES: typing.FrozenSet['FitFrame'] = frozenset(
    list(RECORD_TO_ODICT_MAP.keys())
)


def try_parse_frame(frame: 'FitFrame') -> typing.OrderedDict:
    """Parse a FIT data frame and retun it as an OrderedDict instance.
    """
    for ftype in FRAME_TYPES:
        if isinstance(frame, ftype):  # type: ignore
            return RECORD_TO_ODICT_MAP[ftype](frame)

    raise ValueError(f'Invalid frame: {frame!s}')


def each_frame_from_filepath(stream) -> typing.Iterator[typing.OrderedDict]:
    """Load and make a OrderedDict object for each data frames.

    .. seealso:: fitdecode.cmdfitjson.main
    """
    with fitdecode.FitReader(stream) as reader:
        for frame in reader:
            yield try_parse_frame(frame)


class Parser(anyconfig.backend.base.Parser,
             anyconfig.backend.base.FromStreamLoaderMixin,
             anyconfig.backend.base.BinaryLoaderMixin):
    """
    Loader for fortios (fortigate) "show *configuration" outputs.
    """
    _cid = "fit"
    _type = "fit"
    _extensions = ['fit']
    _ordered = True

    def load_from_stream(self, stream, _container, **kwargs):
        """
        Load config from given file or file-like object `stream`.

        :param stream: A file or file like object of Java properties files
        :param container: callble to make a container object
        :param kwargs: optional keyword parameters (ignored)

        :return: Dict-like object holding config parameters
        """
        return list(each_frame_from_filepath(stream))

    def dump_to_stream(self, cnf, stream, **kwargs):
        """
        Dump config 'cnf' to a file or file-like object 'stream'.

        :param cnf: Java properties config data to dump
        :param stream: FIT data file or file like object
        :param kwargs: backend-specific optional keyword parameters :: dict
        """
        raise NotImplementedError("Not implemented yet")

# vim:sw=4:ts=4:et:
