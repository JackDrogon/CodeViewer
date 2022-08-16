# coding: utf-8

import re

from .utils import remove_anon
from .class_manager import ClassManger
from .namespace import Namespace, NotFoundNamespaceError

GLOBAL_NAMESPACE_NAME = '.'
GLOBAL_NAMESPACE_TAG = {'name': GLOBAL_NAMESPACE_NAME}


class TagManger():

    @staticmethod
    def __is_namespace(kind: str) -> bool:
        return kind == 'namespace'

    @staticmethod
    def __is_class(kind: str) -> bool:
        if kind == 'class':
            return True
        if kind == 'struct':
            return True
        if kind == 'enum':
            return True
        return False

    @staticmethod
    def __is_function(kind: str) -> bool:
        if kind == 'function':
            return True
        return False

    @staticmethod
    def __is_variable(kind: str) -> bool:
        if kind == 'variable':
            return True
        return False

    @staticmethod
    def __is_member(kind: str) -> bool:
        if kind == 'member':
            return True
        if kind == 'enumerator':
            return True
        return False

    def __init__(self) -> None:
        self.tags = {}
        self.class_manager = ClassManger()
        self.function_manger = {}
        self.variable_manger = {}
        self.namespaces = {
            GLOBAL_NAMESPACE_NAME: Namespace(GLOBAL_NAMESPACE_TAG)
        }
        self.classname_to_namespace = {}

    def __lshift__(self, tag) -> None:
        self.tags[tag['name']] = tag
        # kind is class, add to class manager
        kind = tag.get('kind', '')
        if kind == '':
            return
        if self.__is_namespace(kind):
            self.add_namespace(tag)

        namespace = self.__get_namespace(tag)
        if self.__is_class(kind):
            class_name = namespace.add_class(tag)
            self.classname_to_namespace[class_name] = namespace
            return
        # kind is function, add to function manager
        if self.__is_function(kind):
            namespace.add_function(tag)
            return
        # kind is variable, add to variable manager
        if self.__is_variable(kind):
            namespace.add_variable(tag)
            return
        if self.__is_member(kind):
            namespace.add_member(tag)
            return

    """"
    function: add namespace
    """

    def add_namespace(self, tag: dict) -> None:
        namespace = Namespace(tag)
        self.namespaces[namespace.name] = namespace
        if namespace.name in self.namespaces:
            self.namespaces[namespace.name].merge(tag)
        else:
            self.namespaces[namespace.name] = namespace

    def __get_namespace(self, tag: dict) -> Namespace:
        scope_kind = tag.get('scopeKind', None)
        # scope_kind is None
        if scope_kind is None:
            return self.namespaces[GLOBAL_NAMESPACE_NAME]

        if self.__is_class(scope_kind):
            class_name = remove_anon(tag.get('scope', ''))
            class_name = re.sub(r"<.*>", "", class_name)
            if class_name == '':
                return self.namespaces[GLOBAL_NAMESPACE_NAME]

            try:
                return self.classname_to_namespace[class_name]
            except KeyError:
                raise NotFoundNamespaceError(class_name)

        # HACK: for kind: local....
        if not self.__is_namespace(scope_kind):
            return self.namespaces[GLOBAL_NAMESPACE_NAME]

        #  scope_kind is namespace
        scope = tag.get('scope', None)
        if scope is None:
            return self.namespaces[GLOBAL_NAMESPACE_NAME]

        scope = remove_anon(scope)
        if scope == "":
            return self.namespaces[GLOBAL_NAMESPACE_NAME]

        namespace = self.namespaces.get(scope, None)
        if namespace is not None:
            return namespace

        raise NotFoundNamespaceError(f"Not found namespace: {scope}")
