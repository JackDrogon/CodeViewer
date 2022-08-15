# from typing import Self https://peps.python.org/pep-0673/
from __future__ import annotations

import abc
import json
import re
from io import StringIO
"""
PlantUMLer
abstract class with method to_plantuml(), return str
"""


class Buffer:

    def __init__(self):
        self.buffer = StringIO()

    """
    function <<(value), write to buffer
    """

    def __lshift__(self, value: str) -> Buffer:
        self.buffer.write(value)
        return self

    def __str__(self) -> str:
        return self.buffer.getvalue()


class PlantUMLer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_plantuml(self, buffer: Buffer) -> None:
        pass


# {"_type"=>"tag",
#  "name"=>"AcceptAndReply",
#  "path"=>"raft/raft_paper_test.cc",
#  "pattern"=>
#   "/^  static std::unique_ptr<Message> AcceptAndReply(std::unique_ptr<Message> msg) {$/",
#  "file"=>true,
#  "typeref"=>"typename:std::unique_ptr<Message>",
#  "kind"=>"function",
#  "scope"=>"byteraft::ConsensusTest",
#  "scopeKind"=>"class"}


class Symbol(PlantUMLer):

    def __init__(self, tag) -> None:
        self.name = tag['name']
        # FIXME
        self.filename = tag.get('path', "")
        self.line = 0
        self.body = ""

    def __str__(self) -> str:
        return f"{self.name} {self.filename}:{self.line}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_plantuml(self, buffer: Buffer) -> None:
        buffer << self.__str__() << ";"


# maybe to all function
class ClassFunction(Symbol):
    # {"_type": "tag", "name": "leveldb_filterpolicy_create_bloom::Wrapper::CreateFilter", "path": "db/c.cc", "pattern": "/^    void CreateFilter(const Slice* keys, int n, std::string* dst) const {$/", "file": true, "language": "C++", "typeref": "typename:void", "kind": "function", "access": "public", "signature": "(const Slice * keys,int n,std::string * dst) const", "scope": "leveldb_filterpolicy_create_bloom::Wrapper", "scopeKind": "struct"}
    def __init__(self, tag) -> None:
        super().__init__(tag)
        scope = tag.get("scope", None)
        # if name startwiths scope, remove scope prefix
        if scope and self.name.startswith(scope):
            self.name = self.name[len(scope) + 2:]  # +2 is "::"

        # typeref remove typename:
        self.typeref = tag.get("typeref", "")
        if self.typeref.startswith("typename:"):
            self.typeref = self.typeref[len("typename:"):]

        # access uml tag
        access = tag.get("access", "")
        if access == 'private':
            self.access = '-'
        elif access == 'protected':
            self.access = '#'
        else:
            self.access = '+'

        self.signature = tag.get("signature", "")

    def __str__(self) -> str:
        return f"{self.access} {self.typeref} {self.name}{self.signature}"


class Variable(Symbol):

    # {"_type": "tag", "name": "leveldb::VersionEdit::deleted_files_", "path": "db/version_edit.h", "pattern": "/^  DeletedFileSet deleted_files_;$/", "language": "C++", "typeref": "typename:DeletedFileSet", "kind": "member", "access": "private", "scope": "leveldb::VersionEdit", "scopeKind": "class"}
    def __init__(self, tag: dict) -> None:
        super().__init__(tag)
        scope = tag.get("scope", None)
        # if name startwiths scope, remove scope prefix
        if scope and self.name.startswith(scope):
            self.name = self.name[len(scope) + 2:]  # +2 is "::"

        # typeref remove typename:
        self.typeref = tag.get("typeref", "")
        if self.typeref.startswith("typename:"):
            self.typeref = self.typeref[len("typename:"):]

        # access uml tag
        access = tag.get("access", "")
        if access == 'private':
            self.access = '-'
        elif access == 'protected':
            self.access = '#'
        else:
            self.access = '+'

    def __str__(self) -> str:
        return f"{self.access} {self.typeref} {self.name}"


def remove_anon(name: str) -> str:
    # if scope split by ::, any one contains str startwiths "__anon", remove it
    # like leveldb::__anon2cdfda410111::PosixEnv => leveldb::PosixEnv
    for field in name.split("::"):
        if field.startswith("__anon"):
            name = name.replace(f"{field}::", "")
    return name


class Class(Symbol):
    """
    scope = "", class is in global namespace
    """

    def __init__(self, tag) -> None:
        super().__init__(tag)
        self.variables = []
        self.functions = []
        self.inherits = set()
        self.scope = tag.get('scope', "")
        self.is_anon = None

        self.merge(tag)

    """
    function add inherit class
    tag: {"_type": "tag", "name": "T3", "path": "t1.h", "pattern": "/^class T3 : public T1, T2, map<string, int> {};$/", "language": "C++", "kind": "class", "inherits": "T1,T2,map<string,int>"}
    split by ','
    """

    def __add_inherits(self, tag: dict) -> None:
        inherit = tag.get("inherits", None)
        if inherit is None:
            return

        inherits = inherit.split(",")
        self.inherits.update(inherits)
        # for inherit in inherits:
        #     # remove cpp template <type>
        #     # self.inherit[i] = remove_anon(self.inherit[i])
        #     self.inherits.append(inherit)

    # split __init__ in merge by multipass, because some classes inherit from other class && with other
    # generated tag
    def merge(self, tag) -> None:
        if self.is_anon is None:
            self.__maybe_fix_name()

        self.__add_inherits(tag)

    """fix the name of class"""

    def __maybe_fix_name(self):
        # if name not start with scope name, add scope name to the front
        # like DataFile leveldb::SpecialEnv::NewWritableFile => leveldb::SpecialEnv::NewWritableFile::Data
        if not self.name.startswith(self.scope):
            self.name = self.scope + "::" + self.name

        name = remove_anon(self.name)
        if name != self.name:
            self.is_anon = True
            self.name = name
        else:
            self.is_anon = False

    def __str__(self) -> str:
        buffer = Buffer()
        buffer << f"class: {self.name}"
        if len(self.inherits) > 0:
            buffer << "\n"
            buffer << f"inherits: [\n"
            for inherit in self.inherits:
                buffer << f"\t{inherit}\n"
            buffer << f"]"
        if len(self.variables) > 0:
            buffer << "\n"
            buffer << f"members: [\n"
            for variable in self.variables:
                buffer << f"\t{variable}\n"
            buffer << f"]"
        if len(self.functions) > 0:
            buffer << "\n"
            buffer << f"functions: [\n"
            for function in self.functions:
                buffer << f"\t{function}\n"
            buffer << f"]"
        return str(buffer)

    def add_function(self, tag: dict) -> None:
        self.functions.append(ClassFunction(tag))

    def add_variable(self, tag: dict) -> None:
        self.variables.append(Variable(tag))

    # to plantuml
    def to_plantuml(self, buffer: Buffer) -> None:
        buffer << f"class {self.name} {{\n"

        # append functions
        for f in self.functions:
            f.to_plantuml(buffer)
            buffer << '\n'
        if len(self.functions) != 0:
            buffer << '\n'

        # append variables
        for v in self.variables:
            v.to_plantuml(buffer)
            buffer << '\n'

        buffer << '}'


class Namespace():
    pass


class ClassManger():

    def __init__(self) -> None:
        self.classes = {}

    """
    function: add class
    """

    def add_class(self, tag: dict) -> None:
        klass = Class(tag)
        if klass.name in self.classes:
            self.classes[klass.name].merge(tag)
        else:
            self.classes[klass.name] = klass

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

        raise NotFoundClassError(raw_class_name)

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

        # FIXME: map<string, map<int, int>>
        class_name = re.sub(r"<.*>", "", class_name)
        if self.__add_variable(class_name, tag):
            return

        # raise NotFoundClassError(class_name)
        raise NotFoundClassError(raw_class_name)


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


# def show_class(filename: str):
#     file = open(filename, 'r')
#     for line in file:
#         entry = json.loads(line)
#         # print(data['class'])
#         if "kind" in entry and entry['kind'] == 'class':
#             print(entry['name'])


# TODO
class ProgrammgingLanguageManager():

    def __init__(self, name: str) -> None:
        self.name = name


class NotFoundClassError(Exception):

    def __init__(self, message: str) -> None:
        self.message = message


class TagParser():

    def __init__(self, tags_filename: str):
        self.tags_filename = tags_filename

    def add_tags(self, tag_manager: TagManger) -> None:
        # first pass
        second_pass_tags = []
        file = open(self.tags_filename, 'r')
        for line in file:
            tag = json.loads(line)
            if tag.get('language', '') != 'C++':
                continue
            try:
                tag_manager << tag
            except NotFoundClassError:
                second_pass_tags.append(tag)

        # second pass, handle class not found in first pass
        # print("send second pass")
        for tag in second_pass_tags:
            tag_manager << tag
            # try:
            #     tag_manager << tag
            # except NotFoundClassError:
            #     pass
