# coding: utf-8

from .buffer import Buffer
from .symbol import Symbol
from .variable import Variable
from .klass import Class
from .utils import remove_anon
from .class_manager import ClassManger, NotFoundClassError
from .tag_manager import TagManger
from .tag_parser import TagParser
from .namespace import Namespace


# TODO
class ProgrammgingLanguageManager():

    def __init__(self, name: str) -> None:
        self.name = name
