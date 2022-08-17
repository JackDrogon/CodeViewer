#!/usr/bin/env python
# coding: utf-8
""" code_viewer.utils unittest
"""

from code_viewer.utils import remove_anon, remove_template_class_typename

import unittest


class UtilsTest(unittest.TestCase):

    def test_remove_anon(self):
        cases = [
            ("__anon1", ""),
            ("__anon1::__anon2", ""),
            ("__anon1::__anon2::__anon3", ""),
            ("__anon1::__anon2::__anon3::__anon4::__anon5::__anon6::__anon7::__anon8::__anon9::__anon10::__anon11",
             ""),
            ("leveldb::__anon2cdfda410111::PosixEnv", "leveldb::PosixEnv"),
        ]

        for origin_name, name_without_anon in cases:
            self.assertEqual(remove_anon(origin_name), name_without_anon)

    def test_remove_template_class_typename(self):
        self.assertEqual(remove_template_class_typename('std::vector<int>'),
                         'std::vector')
        self.assertEqual(
            remove_template_class_typename('std::vector<int>::iterator'),
            'std::vector::iterator')
        self.assertEqual(
            remove_template_class_typename(
                'std::vector<int, std::allocator<int>>'), 'std::vector')
        self.assertEqual(
            remove_template_class_typename('map<string, map<int, string>>'),
            "map")
        self.assertEqual(
            remove_template_class_typename(
                'map<string, map<int, string>>::iterator'), "map::iterator")
        # self.assertEqual(
        #     remove_template_class_typename(
        #         'map<string, map<int, string>>::iterator<std::string>'),
        #     "map::iterator")
