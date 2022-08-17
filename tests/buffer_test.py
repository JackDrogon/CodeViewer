#!/usr/bin/env python
# coding: utf-8
"""
buffer unittest
"""
import code_viewer

import unittest


class BufferTest(unittest.TestCase):

    def test_buffer(self) -> None:
        cases = [
            "test",
            "test1",
            "test2",
            "",
            "test3",
        ]
        buffer = code_viewer.Buffer()
        s = ""
        for case in cases:
            buffer << case
            s += case
        self.assertEqual(s, str(buffer))
