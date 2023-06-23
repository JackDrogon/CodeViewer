#!/usr/bin/env python3
# coding: utf-8

import logging
from argparse import ArgumentParser

import code_viewer


class ListClassAction:

    def __call__(self, tag_manager: code_viewer.TagManager):
        for namespace in tag_manager.namespaces.values():
            for klass in namespace.class_manager.classes.values():
                print(klass.name)


class ToUmlAction:

    def __call__(self, tag_manager: code_viewer.TagManager):
        for namespace in tag_manager.namespaces.values():
            for klass in namespace.class_manager.classes.values():
                buffer = code_viewer.Buffer()
                klass.to_plantuml(buffer)
                print(buffer)
                print("----------")


class ShowClassAction:

    def __call__(self, tag_manager: code_viewer.TagManager):
        for namespace in tag_manager.namespaces.values():
            logging.debug(f"namespace {namespace.name}")
            for klass in namespace.class_manager.classes.values():
                print(klass.name, klass.scope)
                print(klass)
                print("----------")


class ShowClassInheritsAction:

    class Clazz:

        def __init__(self, name):
            self.name = name
            self.derived_classes = set()

        def add_deriverd_class(self, klass_name: str):
            self.derived_classes.add(klass_name)

    def __init__(self):
        # klasses is a map (name, klass)
        self.klasses = {}

    def __construct_klasses(self, tag_manager: code_viewer.TagManager):
        klasses = self.klasses
        root = self.Clazz(".")
        klasses["."] = root

        # Two phases add to klasses graph
        # Phase 1: add all class symbol in klasses
        for namespace in tag_manager.namespaces.values():
            logging.debug(f"namespace {namespace.name}")
            for klass in namespace.class_manager.classes.values():
                self.klasses[klass.name] = self.Clazz(klass.name)
                if not klass.is_derived_class():
                    root.add_deriverd_class(klass.name)

        # Phase 2: construct inherits relationship
        for namespace in tag_manager.namespaces.values():
            for klass in namespace.class_manager.classes.values():
                if not klass.is_derived_class():
                    continue

                for inherit in klass.inherits:
                    inherit_class_name = code_viewer.utils.remove_anon(f'{klass.scope}::{inherit}')
                    # print(f"{klass.name} inherits from {inherit_class_name}")
                    if inherit_class_name not in klasses:
                        self.klasses[inherit_class_name] = self.Clazz(inherit_class_name)
                        root.add_deriverd_class(inherit_class_name)
                    else:
                        klasses[inherit_class_name].add_deriverd_class(klass.name)

    def __print_class_inherits_graph(self):
        klasses = self.klasses
        # print from root, DFS
        stack = [(klasses["."], 0)]
        while stack:
            klass, level = stack.pop()
            print("|   " * level, end="")
            print("|-- ", end="")
            print(klass.name)
            for derived_class in klass.derived_classes:
                stack.append((klasses[derived_class], level + 1))

    def __call__(self, tag_manager: code_viewer.TagManager):
        self.__construct_klasses(tag_manager)
        self.__print_class_inherits_graph()


def setup_logger(filename: str = None, type: str = "console", level_name: str = "INFO") -> None:
    """
    type is console/console-color/file(all other)
    """
    format = "[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] - %(message)s"
    level = getattr(logging, level_name.upper(), None)
    # level name to level
    if type == "console":
        logging.basicConfig(format=format, level=level_name)
        return
    elif type == "console-color":
        import coloredlogs
        coloredlogs.install(fmt=format, level=level)
        return

    if filename is None:
        import pathlib
        filename = f"{pathlib.Path(__file__).stem}.log"

    logging.basicConfig(format=format, filename=filename, level=level)


def parse_args() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    list_class_parser = subparsers.add_parser('list-class')
    list_class_parser.set_defaults(func=ListClassAction())

    to_uml_parser = subparsers.add_parser('to-uml')
    to_uml_parser.set_defaults(func=ToUmlAction())

    show_class_parser = subparsers.add_parser('show-class')
    show_class_parser.set_defaults(func=ShowClassAction())

    show_class_inherits_parser = subparsers.add_parser('show-class-inherits')
    show_class_inherits_parser.set_defaults(func=ShowClassInheritsAction())

    parser.add_argument('filename')
    # Add log level flag, default "DEBUG"
    parser.add_argument('--log-level', default='DEBUG', help='Set the logging level')
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # setup_logger(type=None) # file logger
    setup_logger(type="console-color", level_name=args.log_level)

    logging.debug(f"run with {args}")
    tag_parser = code_viewer.TagParser(args.filename)
    tag_manager = code_viewer.TagManager()
    tag_parser.add_tags(tag_manager)
    logging.debug(f"tag_manager: {tag_manager}")

    args.func(tag_manager)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
