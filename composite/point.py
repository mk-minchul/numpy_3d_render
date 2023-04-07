import pygame
from primatives.vector import Vector3
from primatives.matrix import Matrix
from primatives.camera import Camera
from constants import ZOFFSET, Width, Height
from transformations import to_pygame_space


class Point():

    def __init__(self, position: Vector3, color=(255,255,255), radius=10):
        self.position = position
        self.color = color
        self.radius = radius

    def transform(self, position_vec: Vector3 = None, transform_mat: Matrix = None):
        position = self.position
        if position_vec is not None:
            position = position + position_vec
        if transform_mat is not None:
            position = position @ transform_mat
        return Point(position, color=self.color, radius=self.radius)

    def update(self, screen, world_position, world_transform, camera, draw_point=True):

        # local to world transform
        transformed: Point = self.transform(world_position, world_transform)

        # view matrix transform
        transformed = transformed.transform(transform_mat=camera.view_matrix)

        # perspective transform
        transformed = transformed.transform(transform_mat=camera.perspective_transform())

        # pygame space
        transformed.position = to_pygame_space(transformed.position)

        if draw_point:
            pygame.draw.circle(screen, self.color, transformed.position.get_xy(), self.radius)
        return transformed