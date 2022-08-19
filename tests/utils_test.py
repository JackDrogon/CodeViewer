# coding: utf-8
""" code_viewer.utils unittest
"""

from code_viewer.utils import remove_anon, remove_template_class_typename, access_to_uml

import unittest


class UtilsTest(unittest.TestCase):

    def test_remove_anon(self):
        cases = [('__anon1', ''), ('__anon1::__anon2', ''), ('__anon1::__anon2::__anon3', ''),
                 ('__anon1::__anon2::__anon3::__anon4::__anon5::__anon6::__anon7::__anon8::__anon9::__anon10::__anon11', ''),
                 ('leveldb::__anon2cdfda410111::PosixEnv', 'leveldb::PosixEnv')]

        for origin_name, name_without_anon in cases:
            self.assertEqual(remove_anon(origin_name), name_without_anon)

    def test_remove_template_class_typename(self):
        cases = [('std::vector<int>', 'std::vector'), ('std::vector<int>::iterator', 'std::vector::iterator'),
                 ('std::vector<int, std::allocator<int>>', 'std::vector'),
                 ('std::vector<int, std::allocator<int>>::iterator', 'std::vector::iterator'),
                 ('map<string, map<int, string>>', 'map'), ('map<string, map<int, string>>::iterator', 'map::iterator'),
                 ('map<string, map<int, string>>::iterator<std::string>', 'map::iterator')]

        for origin_name, name_without_template_typename in cases:
            self.assertEqual(remove_template_class_typename(origin_name), name_without_template_typename)

    def test_access_to_uml(self):
        good_cases = [('private', '-'), ('protected', '#'), ('public', '+')]
        for access, uml_access in good_cases:
            self.assertEqual(access_to_uml(access), uml_access)

        bad_cases = ['', 'invalid']
        for bad_case in bad_cases:
            self.assertRaises(ValueError, access_to_uml, bad_case)
