# coding: utf-8

import re


def remove_anon(name: str) -> str:
    # if scope split by ::, any one contains str startwiths "__anon", remove it
    # like leveldb::__anon2cdfda410111::PosixEnv => leveldb::PosixEnv
    for index, field in enumerate(name.split('::')):
        if not field.startswith("__anon"):
            continue

        if index == 0:
            name = name.replace(field, "")
        else:
            name = name.replace(f"::{field}", "")
    return name


def remove_template_class_typename(class_name: str) -> str:
    """ Parse template class name, remove template class name template typename
    Example:
    >>> remove_template_class_typename("std::vector<int>")
    'std::vector'
    >>> remove_template_class_typename("std::vector<int, std::allocator<int>>")
    'std::vector'
    """
    # FIXME: map<string, map<int, int>>
    pattern = re.compile(r"<.*>")
    return pattern.sub("", class_name)
