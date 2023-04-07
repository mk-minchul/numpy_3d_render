from primatives.vector import Vector3
from composite.triangle import Triangle
from typing import Optional


class Light():

    def __init__(self):
        pass

    def shade(self, triangle: Triangle, normal: Optional[Vector3] = None) -> Triangle:
        raise NotImplementedError()
