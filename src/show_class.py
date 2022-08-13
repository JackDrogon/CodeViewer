#!/usr/bin/env python3

import sys
import json

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


class Symbol():

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


# maybe to all function
class ClassFunction(Symbol):

    def __init__(self, tag) -> None:
        super().__init__(tag)


class Variable(Symbol):

    def __init__(self, tag) -> None:
        super().__init__(tag)


class Class(Symbol):

    def __init__(self, tag) -> None:
        super().__init__(tag)
        self.variables = []
        self.functions = []

    def __str__(self) -> str:
        # FIXME
        # return super().__str__()
        return f"class: {self.name}\nmembers: {self.variables}\nfunctions: {self.functions}"

    def add_function(self, tag: dict) -> None:
        self.functions.append(ClassFunction(tag))

    def add_variable(self, tag: dict) -> None:
        self.variables.append(Variable(tag))


class Namespace():
    pass


class ClassManger():

    def __init__(self) -> None:
        self.classes = {}

    def __lshift__(self, tag: dict) -> Class:
        self.classes[tag['name']] = Class(tag)

    """
    function: add function tag, delegate to class
    """

    def add_function(self, tag: dict) -> None:
        class_name = tag['scope']
        if class_name in self.classes:
            self.classes[class_name].add_function(tag)
        else:
            print(f"{class_name} not found")

    """
    function: add variable tag, delegate to class
    """

    def add_variable(self, tag: dict) -> None:
        class_name = tag['scope']
        if class_name in self.classes:
            self.classes[class_name].add_variable(tag)
        else:
            print(f"{class_name} not found")


class TagManger():

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
        elif kind == 'class':
            self.class_manager << tag
        # kind is function, add to function manager
        elif kind == 'function':
            self.add_function(tag)
        # kind is variable, add to variable manager
        elif kind == 'variable':
            self.add_variable(tag)
        elif kind == 'member':
            self.add_member(tag)

    """
    add function tag

    if function scopeKind is class, call class_manager add function tag
    """

    def add_function(self, tag: dict) -> None:
        if tag.get('scopeKind', '') == 'class':
            self.class_manager.add_function(tag)
        else:
            self.function_manger[tag['name']] = tag

    """
    add variable tag

    if function scopeKind is class, call class_manager add variable tag
    """

    def add_variable(self, tag: dict):
        if tag.get('scopeKind', '') == 'class':
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


class TagParser():

    def __init__(self, tag_manager: TagManger, filename: str):
        self.tag_manager = tag_manager
        self.__add_tags(filename)

    def __add_tags(self, filename: str):
        file = open(filename, 'r')
        for line in file:
            tag = json.loads(line)
            if tag.get('language', '') == 'C++':
                self.tag_manager << tag


def main():
    tag_manager = TagManger()
    tag_parser = TagParser(tag_manager, sys.argv[1])
    print(tag_parser.tag_manager.class_manager.classes)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
