#!/usr/bin/env python3
# coding: utf-8

from argparse import ArgumentParser

import code_viewer


def main():
    parser = ArgumentParser()
    parser.add_argument('--to_uml', action='store_true')
    parser.add_argument('filename')
    args = parser.parse_args()

    tag_parser = code_viewer.TagParser(args.filename)
    tag_manager = code_viewer.TagManger()
    tag_parser.add_tags(tag_manager)
    # print(tag_manager.class_manager.classes)
    for klass in tag_manager.class_manager.classes.values():
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
