# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: audio.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'audio.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0b\x61udio.proto\x12\x0c\x61udioservice\"\x1f\n\x0c\x41udioRequest\x12\x0f\n\x07news_id\x18\x01 \x01(\t\"6\n\rAudioResponse\x12\x12\n\naudio_data\x18\x01 \x01(\x0c\x12\x11\n\tfile_name\x18\x02 \x01(\t\"6\n\x12NewsContentRequest\x12\x0f\n\x07news_id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\t\"7\n\x13NewsContentResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t2\xb6\x01\n\x0c\x41udioService\x12I\n\x0cGetAudioFile\x12\x1a.audioservice.AudioRequest\x1a\x1b.audioservice.AudioResponse\"\x00\x12[\n\x12ReceiveNewsContent\x12 .audioservice.NewsContentRequest\x1a!.audioservice.NewsContentResponse\"\x00\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'audio_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_AUDIOREQUEST']._serialized_start=29
  _globals['_AUDIOREQUEST']._serialized_end=60
  _globals['_AUDIORESPONSE']._serialized_start=62
  _globals['_AUDIORESPONSE']._serialized_end=116
  _globals['_NEWSCONTENTREQUEST']._serialized_start=118
  _globals['_NEWSCONTENTREQUEST']._serialized_end=172
  _globals['_NEWSCONTENTRESPONSE']._serialized_start=174
  _globals['_NEWSCONTENTRESPONSE']._serialized_end=229
  _globals['_AUDIOSERVICE']._serialized_start=232
  _globals['_AUDIOSERVICE']._serialized_end=414
# @@protoc_insertion_point(module_scope)