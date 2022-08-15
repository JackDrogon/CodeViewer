# coding: utf-8

from .class_manager import ClassManger


class TagManger():

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

    def __lshift__(self, tag) -> None:
        self.tags[tag['name']] = tag
        # kind is class, add to class manager
        kind = tag.get('kind', '')

        if kind == '':
            return
        elif self.__is_class(kind):
            self.add_class(tag)
        # kind is function, add to function manager
        elif self.__is_function(kind):
            self.add_function(tag)
        # kind is variable, add to variable manager
        elif self.__is_variable(kind):
            self.add_variable(tag)
        elif self.__is_member(kind):
            self.add_member(tag)

    """
    function: add class tag to class manager
    """

    def add_class(self, tag: dict) -> None:
        self.class_manager.add_class(tag)

    """
    add function tag

    if function scopeKind is class, call class_manager add function tag
    """

    def add_function(self, tag: dict) -> None:
        scope_kind = tag.get('scopeKind', '')
        if scope_kind == 'class' or scope_kind == 'struct':
            self.class_manager.add_function(tag)
        else:
            self.function_manger[tag['name']] = tag

    """
    add variable tag

    if function scopeKind is class, call class_manager add variable tag
    """

    def add_variable(self, tag: dict):
        scope_kind = tag.get('scopeKind', '')
        if scope_kind == 'class' or scope_kind == 'struct':
            self.class_manager.add_variable(tag)
        else:
            self.variable_manger[tag['name']] = tag

    def add_member(self, tag: dict):
        self.class_manager.add_variable(tag)
