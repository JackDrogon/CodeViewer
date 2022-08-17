# coding: utf-8

import re


def remove_anon(name: str) -> str:
    """ Parse name, remove anonymous namespace
    if scope split by ::, any one contains str startwiths "__anon", remove it
    >>> remove_anon("__anon1")
    ''
    >>> remove_anon("__anon1::__anon2")
    ''
    >>> remove_anon("leveldb::__anon2cdfda410111::PosixEnv")
    'leveldb::PosixEnv'
    """
    namespace_and_class = []
    for index, field in enumerate(name.split('::')):
        if field.startswith("__anon"):
            continue
        namespace_and_class.append(field)

    return "::".join(namespace_and_class)


def remove_template_class_typename(class_name: str) -> str:
    """ Parse template class name, remove template class name template typename
    Example:
    >>> remove_template_class_typename("std::vector<int>")
    'std::vector'
    >>> remove_template_class_typename("std::vector<int, std::allocator<int>>")
    'std::vector'
    >>> remove_template_class_typename('map<string, map<int, string>>::iterator<std::string>')
    'map::iterator'
    """
    # FIXME: map<string, map<int, string>>::iterator<std::string>
    pattern = re.compile(r"<.*>")
    return pattern.sub("", class_name)
