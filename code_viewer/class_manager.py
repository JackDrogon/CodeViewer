# coding: utf-8

from .klass import Class
from .utils import remove_anon, remove_template_class_typename


class NotFoundClassError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message


class ClassManger():

    def __init__(self) -> None:
        self.classes = {}

    """
    function: add class, return class name
    """

    def add_class(self, tag: dict) -> str:
        klass = Class(tag)
        if klass.name in self.classes:
            self.classes[klass.name].merge(tag)
        else:
            self.classes[klass.name] = klass
        return klass.name

    def __add_function(self, class_name: str, tag: dict) -> bool:
        if class_name in self.classes:
            self.classes[class_name].add_function(tag)
            return True
        return False

    """
    function: add function tag, delegate to class
    """

    def add_function(self, tag: dict) -> None:
        raw_class_name = tag['scope']
        if self.__add_function(raw_class_name, tag):
            return

        # FIXME: need to check scope is anon class
        # check tag is in cpp impl file not header
        class_name = remove_anon(raw_class_name)
        if self.__add_function(class_name, tag):
            return

        raise NotFoundClassError(f"Not found class: {raw_class_name}")

    def __add_variable(self, class_name: str, tag: dict) -> bool:
        if class_name in self.classes:
            self.classes[class_name].add_variable(tag)
            return True
        return False

    """
    function: add variable tag, delegate to class
    """

    def add_variable(self, tag: dict) -> None:
        raw_class_name = tag['scope']
        if self.__add_variable(raw_class_name, tag):
            return

        # FIXME: need to check scope is anon class
        # check tag is in cpp impl file not header
        class_name = remove_anon(raw_class_name)
        if self.__add_variable(class_name, tag):
            return

        class_name = remove_template_class_typename(class_name)
        if self.__add_variable(class_name, tag):
            return

        # raise NotFoundClassError(class_name)
        raise NotFoundClassError(raw_class_name)
