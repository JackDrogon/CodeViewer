#!/usr/bin/env python3
# coding: utf-8

import logging
from argparse import ArgumentParser

import code_viewer


def setup_logger(filename=None, type="console"):
    """
    type is console/console-color/file(all other)
    """
    format = "[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] - %(message)s"
    if type == "console":
        logging.basicConfig(format=format, level=logging.INFO)
        return
    elif type == "console-color":
        import coloredlogs
        coloredlogs.install(format=format, level="INFO")
        return

    if filename is None:
        import pathlib
        filename = f"{pathlib.Path(__file__).stem}.log"

    logging.basicConfig(format=format, filename=filename, level=logging.INFO)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--to-uml', dest="to_uml", action='store_true')
    parser.add_argument('filename')
    parser.add_argument('--list-class', dest="list_class", action='store_true')
    return parser.parse_args()


def list_class(tag_manager: code_viewer.TagManager):
    for namespace in tag_manager.namespaces.values():
        for klass in namespace.class_manager.classes.values():
            print(klass.name)


def main():
    setup_logger(type="console-color")
    # setup_logger(type=None) # file logger

    args = parse_args()

    logging.debug(f"run with {args}")
    tag_parser = code_viewer.TagParser(args.filename)
    tag_manager = code_viewer.TagManager()
    tag_parser.add_tags(tag_manager)

    if args.list_class:
        list_class(tag_manager)
        return

    for namespace in tag_manager.namespaces.values():
        print(f"namespace {namespace.name}")
        for klass in namespace.class_manager.classes.values():
            if args.to_uml:
                buffer = code_viewer.Buffer()
                klass.to_plantuml(buffer)
                print(buffer)
                print("----------")
            else:
                print(klass.name, klass.scope)
                print(klass)
                print("----------")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
