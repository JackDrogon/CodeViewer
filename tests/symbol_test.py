# coding: utf-8
"""
class Symbol unittest
"""

from code_viewer import Symbol

import unittest

from test_helper import to_plantuml


class SymbolTest(unittest.TestCase):
    """
    test: create symbol from tag
    """

    TAG = {
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

    def test_symobol_create(self) -> None:
        symbol = Symbol(self.TAG)

        # check all fields of symbol are set correctly
        self.assertEqual(symbol.name, "leveldb::VersionEdit::deleted_files_")
        self.assertEqual(symbol.kind, "member")
        self.assertEqual(symbol.line, 0)
        self.assertEqual(symbol.filename, "db/version_edit.h")
        self.assertEqual(symbol.body, "")
        self.assertEqual(str(symbol), 'leveldb::VersionEdit::deleted_files_ db/version_edit.h:0')

    def test_symbol_str(self) -> None:
        symbol = Symbol(self.TAG)

        self.assertEqual(to_plantuml(symbol), 'leveldb::VersionEdit::deleted_files_ db/version_edit.h:0;')
