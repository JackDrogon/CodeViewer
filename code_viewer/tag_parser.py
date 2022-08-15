# coding: utf-8

import json

from .class_manager import NotFoundClassError
from .tag_manager import TagManger


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
