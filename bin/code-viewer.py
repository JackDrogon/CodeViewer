#!/usr/bin/env python3
# coding: utf-8

from argparse import ArgumentParser
import logging

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


def main():
    setup_logger(type="console-color")
    # setup_logger(type=None) # file logger

    parser = ArgumentParser()
    parser.add_argument('--to_uml', action='store_true')
    parser.add_argument('filename')
    args = parser.parse_args()

    logging.debug(f"run with {args}")
    tag_parser = code_viewer.TagParser(args.filename)
    tag_manager = code_viewer.TagManger()
    tag_parser.add_tags(tag_manager)
    for namespace in tag_manager.namespaces.values():
        logging.info(f"namespace {namespace.name}")
        for klass in namespace.class_manager.classes.values():
            if args.to_uml:
                buffer = code_viewer.Buffer()
                klass.to_plantuml(buffer)
                print(buffer)
                logging.info("----------")
            else:
                print(klass.name, klass.scope)
                print(klass)
                logging.info("----------")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
