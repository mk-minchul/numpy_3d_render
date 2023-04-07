from light.base import Light
from primatives.vector import Vector3
from composite.triangle import Triangle
from typing import Optional
from constants import DARK


class DirectionalLight(Light):
    '''
    A simple directional light that changes the intensity of the triangle colors based on
    the angle between the triangle normal and the light direction.
    '''

    def __init__(self, position: Vector3, disable=False):
        super(DirectionalLight, self).__init__()
        self.position = position
        self.direction = position.normalize()

    def shade(self, triangle: Triangle, normal: Optional[Vector3] = None) -> Triangle:
        if normal is None:
            normal = triangle.get_normal_vec()

        intesnity = max(self.direction.dot(normal), DARK)
        triangle.color = tuple(int(v*intesnity) for v in triangle.color)
        return triangle