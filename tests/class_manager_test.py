# coding: utf-8
""" code_viewer.ClassManager unittest
"""

import unittest

from test_helper import to_plantuml

from code_viewer import ClassManager, NotFoundClassError


class ClassManagerTest(unittest.TestCase):
    CLASS_TAG = {
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

    MERGE_TAG = {
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

    MEMBER_TAG = {
        "_type": "tag",
        "name": "leveldb::KeyConvertingIterator::iter_",
        "path": "table/table_test.cc",
        "pattern": "/^  Iterator* iter_;$/",
        "file": True,
        "language": "C++",
        "typeref": "typename:Iterator *",
        "kind": "member",
        "access": "private",
        "scope": "leveldb::KeyConvertingIterator",
        "scopeKind": "class"
    }

    FUNCTION_TAG = {
        "_type": "tag",
        "name": "status",
        "path": "table/table_test.cc",
        "pattern": "/^  Status status() const override {$/",
        "file": True,
        "language": "C++",
        "typeref": "typename:Status",
        "kind": "function",
        "access": "public",
        "signature": "() const",
        "scope": "leveldb::KeyConvertingIterator",
        "scopeKind": "class"
    }

    def test_class_manager_add_class(self):
        class_manager = ClassManager()

        klass_name = class_manager.add_class(self.CLASS_TAG)

        self.assertEqual(klass_name, "leveldb::KeyConvertingIterator")
        self.assertEqual(len(class_manager.classes), 1)
        self.assertTrue(klass_name in class_manager.classes)
        klass = class_manager.classes[klass_name]
        self.assertEqual(klass.name, "leveldb::KeyConvertingIterator")
        self.assertEqual(len(klass.inherits), 0)

    def test_class_manager_add_merge_class(self):
        class_manager = ClassManager()
        class_manager.add_class(self.CLASS_TAG)

        klass_name = class_manager.add_class(self.MERGE_TAG)

        self.assertEqual(klass_name, "leveldb::KeyConvertingIterator")
        self.assertEqual(len(class_manager.classes), 1)
        self.assertTrue(klass_name in class_manager.classes)
        klass = class_manager.classes[klass_name]
        self.assertEqual(len(klass.inherits), 1)
        self.assertIn("Iterator", klass.inherits)
        klass_str = """class: leveldb::KeyConvertingIterator
inherits: [
	Iterator
]"""
        self.assertEqual(str(klass), klass_str)
        self.assertEqual(to_plantuml(klass), 'class leveldb::KeyConvertingIterator {\n}')

    def test_class_manager_add_function_with_noexist_classname(self):
        class_manager = ClassManager()
        self.assertRaises(NotFoundClassError, class_manager.add_function, self.FUNCTION_TAG)

    def test_class_manager_add_function(self):
        class_manager = ClassManager()
        class_manager.add_class(self.CLASS_TAG)

        class_manager.add_function(self.FUNCTION_TAG)
        klass = class_manager.classes['leveldb::KeyConvertingIterator']
        klass_str = """class: leveldb::KeyConvertingIterator
functions: [
	public Status status() const
]"""
        self.assertEqual(str(klass), klass_str)
        klass_plantuml_str = """class leveldb::KeyConvertingIterator {
	+ Status status() const;
}"""
        self.assertEqual(to_plantuml(klass), klass_plantuml_str)

    def test_class_manager_add_variable(self):
        class_manager = ClassManager()
        class_manager.add_class(self.CLASS_TAG)

        class_manager.add_variable(self.MEMBER_TAG)

        klass = class_manager.classes['leveldb::KeyConvertingIterator']
        self.assertEqual(len(klass.variables), 1)
        klass_str = '''class: leveldb::KeyConvertingIterator
members: [
	private Iterator * iter_
]'''
        self.assertEqual(str(klass), klass_str)
        klass_uml_str = '''class leveldb::KeyConvertingIterator {
	- Iterator * iter_;
}'''
        self.assertEqual(to_plantuml(klass), klass_uml_str)
