# coding: utf-8

from code_viewer import Buffer, PlantUMLer


def to_plantuml(s: PlantUMLer) -> str:
    buffer = Buffer()
    s.to_plantuml(buffer)
    return str(buffer)
