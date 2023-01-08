# coding: utf-8

import json

from .class_manager import NotFoundClassError
from .tag_manager import TagManager
from .namespace import NotFoundNamespaceError


class TagParser():

    def __init__(self, tags_filename: str):
        self.tags_filename = tags_filename

    def add_tags(self, tag_manager: TagManager) -> None:
        # first pass, construct all namespace, part class && ...
        second_pass_tags = []
        file = open(self.tags_filename, 'r')
        for line in file:
            tag = json.loads(line)
            if tag.get('language', '') != 'C++':
                continue
            try:
                tag_manager << tag
            except (NotFoundNamespaceError, NotFoundClassError):
                second_pass_tags.append(tag)

        # second pass, handle namespace/class not found in first pass
        # construct all class && ...
        # print("send second pass")
        thrid_pass_tags = []
        for tag in second_pass_tags:
            try:
                tag_manager << tag
            except NotFoundClassError:
                thrid_pass_tags.append(tag)

        # construct all somethings else
        # thrid pass, handle class not found in second pass
        # print("send thrid pass")
        for tag in thrid_pass_tags:
            # tag_manager << tag
            try:
                tag_manager << tag
            except NotFoundClassError as e:
                print(e, tag)
                raise e
