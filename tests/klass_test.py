# coding: utf-8
""" code_vieewer ClassFunction && Class unittest
"""

from code_viewer import Class, ClassFunction, klass
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
        self.assertEqual(func.access, "public")
        self.assertEqual(func.signature,
                         "(const Slice * keys,int n,std::string * dst) const")

    def test_class_function_str(self):
        func = ClassFunction(self.TAGS)

        self.assertEqual(
            str(func),
            "public void CreateFilter(const Slice * keys,int n,std::string * dst) const"
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

    def test_klass_add_function(self) -> None:
        klass = Class(self.TAG)
        function_tag = {
            '_type': 'tag',
            'name': 'restarts_',
            'path': 'table/block_builder.h',
            'pattern':
            '/^  std::vector<uint32_t> restarts_;  \\/\\/ Restart points$/',
            'language': 'C++',
            'typeref': 'typename:std::vector<uint32_t>',
            'kind': 'member',
            'access': 'private',
            'scope': 'leveldb::BlockBuilder',
            'scopeKind': 'class'
        }
        # func = ClassFunction(function_tag)

        klass.add_function(function_tag)
        self.assertEqual(len(klass.functions), 1)
        kclass_str = '''class: leveldb::BlockBuilder
functions: [
	private std::vector<uint32_t> restarts_
]'''
        self.assertEqual(str(klass), kclass_str)

    def test_klass_add_variable(self) -> None:
        klass = Class(self.TAG)
        member_tag = {
            '_type': 'tag',
            'name': 'restarts_',
            'path': 'table/block_builder.h',
            'pattern':
            '/^  std::vector<uint32_t> restarts_;  \\/\\/ Restart points$/',
            'language': 'C++',
            'typeref': 'typename:std::vector<uint32_t>',
            'kind': 'member',
            'access': 'private',
            'scope': 'leveldb::BlockBuilder',
            'scopeKind': 'class'
        }

        klass.add_variable(member_tag)
        self.assertEqual(len(klass.variables), 1)
        klass_str = '''class: leveldb::BlockBuilder
members: [
	private std::vector<uint32_t> restarts_
]'''
        self.assertEqual(str(klass), klass_str)

    def test_klass_merge(self) -> None:
        tag = {
            "_type": "tag",
            "name": "KeyConvertingIterator",
            "path": "table/table_test.cc",
            "pattern": "/^class KeyConvertingIterator : public Iterator {$/",
            "file": True,
            "language": "C++",
            "kind": "class",
            "scope": "leveldb",
            "scopeKind": "namespace"
        }
        klass = Class(tag)
        self.assertEqual(klass.name, "leveldb::KeyConvertingIterator")
        self.assertEqual(len(klass.inherits), 0)

        merge_tag = {
            "_type": "tag",
            "name": "KeyConvertingIterator",
            "path": "table/table_test.cc",
            "pattern": "/^class KeyConvertingIterator : public Iterator {$/",
            "file": True,
            "language": "C++",
            "kind": "class",
            "inherits": "Iterator",
            "scope": "leveldb",
            "scopeKind": "namespace"
        }
        klass.merge(merge_tag)
        self.assertEqual(len(klass.inherits), 1)
        self.assertIn("Iterator", klass.inherits)
