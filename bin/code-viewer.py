#!/usr/bin/env python3

import sys

import code_viewer


def main():
    tag_parser = code_viewer.TagParser(sys.argv[1])
    tag_manager = code_viewer.TagManger()
    tag_parser.add_tags(tag_manager)
    # print(tag_manager.class_manager.classes)
    for klass in tag_manager.class_manager.classes.values():
        print(klass.name, klass.scope)
        print(klass)
        print("----------")

        # buffer = Buffer()
        # klass.to_plantuml(buffer)
        # print(buffer)
        # print("----------")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
