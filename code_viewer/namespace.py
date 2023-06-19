# coding: utf-8

from .class_manager import ClassManager
from .symbol import Symbol
from .utils import remove_anon


class NotFoundNamespaceError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message


class Namespace(Symbol):
    """
    not contain filename, line, body
    """

    def __init__(self, tag: dict) -> None:
        super().__init__(tag)
        self.scope = tag.get('scope', "")
        self.class_manager = ClassManager()
        self.function_manger = {}
        self.variable_manger = {}

        self._maybe_fix_name()

    def _maybe_fix_name(self):
        # if name not start with scope name, add scope name to the front
        # like Table leveldb::DB => leveldb::DB::Table
        if not self.name.startswith(self.scope):
            self.name = self.scope + "::" + self.name

        name = remove_anon(self.name)
        if name != self.name:
            self.is_anon = True
            self.name = name
        else:
            self.is_anon = False

    # TODO(Drogon): combine file_name and line_number
    def merge(self, tag: dict) -> None:
        pass

    def add_class(self, tag: dict) -> str:
        return self.class_manager.add_class(tag)

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
