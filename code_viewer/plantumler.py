# coding: utf-8
"""
PlantUMLer
abstract class with method to_plantuml(), return str
"""

import abc

from .buffer import Buffer


class PlantUMLer(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def to_plantuml(self, buffer: Buffer) -> None:
        pass
