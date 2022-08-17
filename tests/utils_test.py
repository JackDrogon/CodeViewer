#!/usr/bin/env python
# coding: utf-8
""" code_viewer.utils unittest
"""

import code_viewer
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
            self.assertEqual(code_viewer.remove_anon(origin_name),
                             name_without_anon)
