#!/usr/bin/env python3
# coding: utf-8

import logging
from argparse import ArgumentParser

import code_viewer


class ListClassAction:

    def __init__(self, tag_manager: code_viewer.TagManager):
        self.tag_manager = tag_manager

    def __call__(self, args):
        for namespace in self.tag_manager.namespaces.values():
            for klass in namespace.class_manager.classes.values():
                print(klass.name)


class ToUmlAction:

    def __init__(self, tag_manager: code_viewer.TagManager):
        self.tag_manager = tag_manager

    def __call__(self, args):
        for namespace in self.tag_manager.namespaces.values():
            for klass in namespace.class_manager.classes.values():
                buffer = code_viewer.Buffer()
                klass.to_plantuml(buffer)
                print(buffer)
                print("----------")


class ShowClassAction:

    def __init__(self, tag_manager: code_viewer.TagManager):
        self.tag_manager = tag_manager

    def __call__(self, args):
        for namespace in self.tag_manager.namespaces.values():
            print(f"namespace {namespace.name}")
            for klass in namespace.class_manager.classes.values():
                print(klass.name, klass.scope)
                print(klass)
                print("----------")


def setup_logger(filename: str = None, type: str = "console") -> None:
    """
    type is console/console-color/file(all other)
    """
    format = "[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] - %(message)s"
    if type == "console":
        logging.basicConfig(format=format, level=logging.INFO)
        return
    elif type == "console-color":
        import coloredlogs
        coloredlogs.install(fmt=format, level="INFO")
        return

    if filename is None:
        import pathlib
        filename = f"{pathlib.Path(__file__).stem}.log"

    logging.basicConfig(format=format, filename=filename, level=logging.INFO)


def parse_args() -> ArgumentParser:
    parser = ArgumentParser()
    subparsers = parser.add_subparsers()

    list_class_parser = subparsers.add_parser('list-class')
    list_class_parser.set_defaults(func=ListClassAction(code_viewer.TagManager()))

    to_uml_parser = subparsers.add_parser('to-uml')
    to_uml_parser.set_defaults(func=ToUmlAction(code_viewer.TagManager()))

    show_class_parser = subparsers.add_parser('show-class')
    show_class_parser.set_defaults(func=ShowClassAction(code_viewer.TagManager()))

    parser.add_argument('filename')
    return parser.parse_args()


def main() -> None:
    setup_logger(type="console-color")
    # setup_logger(type=None) # file logger

    args = parse_args()

    logging.debug(f"run with {args}")
    tag_parser = code_viewer.TagParser(args.filename)
    tag_manager = code_viewer.TagManager()
    tag_parser.add_tags(tag_manager)

    args.func(args)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
