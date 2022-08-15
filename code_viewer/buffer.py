# coding: utf-8

# from typing import Self https://peps.python.org/pep-0673/
from __future__ import annotations

from io import StringIO


class Buffer:

    def __init__(self):
        self.buffer = StringIO()

    """
    function <<(value), write to buffer
    """

    def __lshift__(self, value: str) -> Buffer:
        self.buffer.write(value)
        return self

    def __str__(self) -> str:
        return self.buffer.getvalue()
