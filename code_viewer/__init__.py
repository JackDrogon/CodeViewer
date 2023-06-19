# coding: utf-8

from . import utils
from .buffer import Buffer
from .class_manager import ClassManager, NotFoundClassError
from .klass import Class, ClassFunction
from .namespace import Namespace
from .plantumler import PlantUMLer
from .symbol import Symbol
from .tag_manager import TagManager
from .tag_parser import TagParser
from .variable import Variable


# TODO
class ProgrammgingLanguageManager():

    def __init__(self, name: str) -> None:
        self.name = name
