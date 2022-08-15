# coding: utf-8

from .buffer import Buffer
from .plantumler import PlantUMLer


class Symbol(PlantUMLer):

    def __init__(self, tag) -> None:
        self.name = tag['name']
        # FIXME
        self.filename = tag.get('path', "")
        self.line = 0
        self.body = ""

    def __str__(self) -> str:
        return f"{self.name} {self.filename}:{self.line}"

    def __repr__(self) -> str:
        return self.__str__()

    def to_plantuml(self, buffer: Buffer) -> None:
        buffer << self.__str__() << ";"
