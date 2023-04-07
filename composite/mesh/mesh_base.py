from primatives.vector import Vector3
from primatives.matrix import Matrix
from composite.triangle import Triangle
from typing import Tuple, List
from constants import ZOFFSET, Width, Height
from light.base import Light
from primatives.camera import Camera
import draw

class Mesh():
    def __init__(self,
                 position: Vector3 = Vector3(0, 0, 0),
                 scale: float = 1.0,
                 color: Tuple = (255, 255, 255),
                 transform=Matrix.identity(),
                 triangles: List[Triangle] = []):

        self.position = position
        self.scale = scale
        self.color = color
        self.transform = transform
        self.triangles = triangles

    def update(self, screen, camera: Camera, light: Light):
        # mesh update is iterating through all triangles
        returns = []
        for index, triangle in enumerate(self.triangles):
            _triangles = triangle.update(screen=screen,
                                         camera=camera,
                                         light=light,
                                         world_position=self.position,
                                         world_transform=self.transform,
                                         )
            returns.extend(_triangles)
        return returns