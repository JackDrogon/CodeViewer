# coding: utf-8
""" test namespace class
"""

from code_viewer import Namespace

import unittest

from test_helper import to_plantuml


class NamespaceTest(unittest.TestCase):
    """ test namespace class
    """

    def test_namespace_create(self):
        """ test namespace create
        """
        tag = {"name": "leveldb", "kind": "namespace"}
        namespace = Namespace(tag)
        self.assertEqual(namespace.name, "leveldb")
        self.assertEqual(namespace.scope, "")
        self.assertFalse(namespace.is_anon)
        # self.assertEqual(namespace.path, "")
        # self.assertEqual(namespace.language, "")

    def test_namespace_complex_create(self):
        tag = {
            "_type": "tag",
            "name": "__anon008c292b0111",
            "path": "benchmarks/db_bench.cc",
            "pattern": "/^namespace {$/",
            "file": True,
            "language": "C++",
            "kind": "namespace",
            "scope": "leveldb",
            "scopeKind": "namespace"
        }
        namespace = Namespace(tag)
        self.assertEqual(namespace.name, "leveldb")
        self.assertEqual(namespace.scope, "leveldb")
        self.assertTrue(namespace.is_anon)

    # def test_namespace_str(self):
    #     """ test namespace str
    #     """
    #     tag = {"name": "leveldb", "kind": "namespace"}
    #     namespace = Namespace(tag)
    #     print(namespace)
    #     # self.assertEqual(str(namespace), "namespace leveldb")

    # def test_namespace_plantuml(self):
    #     """ test namespace plantuml
    #     """
    #     namespace = Namespace("leveldb")
    #     # self.assertEqual(to_plantuml(namespace), "namespace leveldb")
