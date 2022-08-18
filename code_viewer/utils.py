# coding: utf-8

from .buffer import Buffer


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
    for field in name.split('::'):
        if field.startswith("__anon"):
            continue
        namespace_and_class.append(field)

    return "::".join(namespace_and_class)


def remove_template_class_typename(class_name: str) -> str:
    """ Parse template class name, remove template class name template typename
    assume class_name is template class name, the class_name is right && valid, guaranteed by caller
    remove '<>' bracket wrapper content
    Example:
    >>> remove_template_class_typename("std::vector<int>")
    'std::vector'
    >>> remove_template_class_typename("std::vector<int, std::allocator<int>>")
    'std::vector'
    >>> remove_template_class_typename('map<string, map<int, string>>::iterator<std::string>')
    'map::iterator'
    """
    buffer = Buffer()
    brace_keep_cnt = 0
    for c in class_name:
        if c == '<':
            brace_keep_cnt += 1
            continue
        if c == '>':
            brace_keep_cnt -= 1
            continue
        if brace_keep_cnt == 0:
            buffer << c

    return str(buffer)


def access_to_uml(access: str) -> str:
    """ Convert access to uml access
    >>> convert_access_to_uml("private")
    '-'
    >>> convert_access_to_uml("protected")
    '#'
    >>> convert_access_to_uml("public")
    '+'
    """
    if access == "private":
        return "-"
    elif access == "protected":
        return "#"
    elif access == "public":
        return "+"
    else:
        raise ValueError(f"Invalid access {access}")
