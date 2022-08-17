#!/usr/bin/env python
# coding: utf-8

from code_viewer import Symbol
from code_viewer import Buffer

import unittest
"""
class Symbol test
test Symbol class
"""


class SymbolTest(unittest.TestCase):

    def test_symbol(self) -> None:
        tag = {
            "_type": "tag",
            "name": "leveldb::VersionEdit::deleted_files_",
            "path": "db/version_edit.h",
            "pattern": "/^  DeletedFileSet deleted_files_;$/",
            "language": "C++",
            "typeref": "typename:DeletedFileSet",
            "kind": "member",
            "access": "private",
            "scope": "leveldb::VersionEdit",
            "scopeKind": "class"
        }
        symbol = Symbol(tag)
        self.assertEqual(symbol.name, "leveldb::VersionEdit::deleted_files_")
        self.assertEqual(symbol.line, 0)
        self.assertEqual(symbol.filename, "db/version_edit.h")
        self.assertEqual(symbol.body, "")
        self.assertEqual(
            str(symbol),
            'leveldb::VersionEdit::deleted_files_ db/version_edit.h:0')

        buffer = Buffer()
        symbol.to_plantuml(buffer)
        self.assertEqual(
            str(buffer),
            'leveldb::VersionEdit::deleted_files_ db/version_edit.h:0;')
