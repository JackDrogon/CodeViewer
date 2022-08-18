# coding: utf-8
""" code_viewer.variable unittest
"""

from code_viewer.variable import Variable

import unittest

from test_helper import to_plantuml


class VariableTest(unittest.TestCase):
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

    def test_variable_create(self):
        v = Variable(self.TAG)
        self.assertEqual(v.name, "deleted_files_")
        self.assertEqual(v.typeref, "DeletedFileSet")
        self.assertEqual(v.access, "private")
        self.assertEqual(v.scope, "leveldb::VersionEdit")
        # self.assertEqual(v.scopeKind, "class")

    def test_variable_str(self):
        v = Variable(self.TAG)
        self.assertEqual(str(v), "private DeletedFileSet deleted_files_")

    def test_variable_plantuml(self):
        v = Variable(self.TAG)
        self.assertEqual(to_plantuml(v), "- DeletedFileSet deleted_files_;")
