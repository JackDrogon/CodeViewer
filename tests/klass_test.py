# coding: utf-8
""" code_vieewer ClassFunction && Class unittest
"""

from code_viewer import Class, ClassFunction
from code_viewer import Buffer

import unittest

from test_helper import to_plantuml


class ClassFunctionTest(unittest.TestCase):
    TAGS = {
        "_type": "tag",
        "name": "leveldb_filterpolicy_create_bloom::Wrapper::CreateFilter",
        "path": "db/c.cc",
        "pattern":
        "/^    void CreateFilter(const Slice* keys, int n, std::string* dst) const {$/",
        "file": True,
        "language": "C++",
        "typeref": "typename:void",
        "kind": "function",
        "access": "public",
        "signature": "(const Slice * keys,int n,std::string * dst) const",
        "scope": "leveldb_filterpolicy_create_bloom::Wrapper",
        "scopeKind": "struct"
    }

    def test_class_function_create(self):
        func = ClassFunction(self.TAGS)

        self.assertEqual(func.name, "CreateFilter")
        self.assertEqual(func.scope,
                         "leveldb_filterpolicy_create_bloom::Wrapper")
        self.assertEqual(func.typeref, "void")
        self.assertEqual(func.access, "+")
        self.assertEqual(func.signature,
                         "(const Slice * keys,int n,std::string * dst) const")

    def test_class_function_str(self):
        func = ClassFunction(self.TAGS)

        self.assertEqual(
            str(func),
            "+ void CreateFilter(const Slice * keys,int n,std::string * dst) const"
        )

    def test_class_function_plantuml(self):
        func = ClassFunction(self.TAGS)

        self.assertEqual(
            to_plantuml(func),
            "+ void CreateFilter(const Slice * keys,int n,std::string * dst) const;"
        )


class ClassTest(unittest.TestCase):
    """
    test: create class from tag
    """

    TAG = {
        "_type": "tag",
        "name": "BlockBuilder",
        "path": "table/block_builder.h",
        "pattern": "/^class BlockBuilder {$/",
        "language": "C++",
        "kind": "class",
        "scope": "leveldb",
        "scopeKind": "namespace"
    }

    # def setUp(self) -> None:
    #     super().setUp()
    #     self.klass = Class(tag)

    # def tearDown(self) -> None:
    #     super().tearDown()
    #     self.klass = None

    def test_klass_create(self) -> None:
        klass = Class(self.TAG)

        # check all fields of symbol are set correctly
        self.assertEqual(klass.name, "leveldb::BlockBuilder")
        self.assertEqual(klass.kind, "class")
        self.assertEqual(klass.line, 0)
        self.assertEqual(klass.filename, "table/block_builder.h")
        self.assertEqual(klass.body, "")
        # TODO(Drogon): other fileds
        # self.assertEqual(klass)

    def test_empty_klass_str(self) -> None:
        klass = Class(self.TAG)

        self.assertEqual(str(klass), 'class: leveldb::BlockBuilder')

    def test_empty_klass_plantuml(self) -> None:
        klass = Class(self.TAG)
        buffer = Buffer()

        klass.to_plantuml(buffer)
        self.assertEqual(str(buffer), 'class leveldb::BlockBuilder {\n}')
