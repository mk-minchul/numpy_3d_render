from __future__ import annotations

import numpy as np

from primatives.vector import Vector3
from primatives.matrix import Matrix
from typing import Tuple, Union
import copy
from ops import signed_dist, plane_line_intersectiion
from typing import List
from constants import ZOFFSET, Width, Height

from transformations import to_pygame_space

class Triangle():

    def __init__(self, v1: Vector3, v2: Vector3, v3: Vector3, color: Tuple = (255, 255, 255)):
        self.vertex1 = v1
        self.vertex2 = v2
        self.vertex3 = v3
        self.color = color

    def transform(self, position_vec: Vector3 = None, transform_mat: Matrix = None):
        vertex1 = self.vertex1
        vertex2 = self.vertex2
        vertex3 = self.vertex3
        if position_vec is not None:
            vertex1 = vertex1 + position_vec
            vertex2 = vertex2 + position_vec
            vertex3 = vertex3 + position_vec
        if transform_mat is not None:
            vertex1 = vertex1 @ transform_mat
            vertex2 = vertex2 @ transform_mat
            vertex3 = vertex3 @ transform_mat

        return Triangle(v1=vertex1, v2=vertex2, v3=vertex3, color=copy.copy(self.color))

    def get_normal_vec(self):
        line1 = self.vertex2 - self.vertex1
        line2 = self.vertex3 - self.vertex1
        normal_vec = (line1.cross_product(line2)).normalize()
        return normal_vec

    def clip(self,
             clipspace_pos: Vector3 = Vector3(0, 0, 1.5),
             clipspace_normal: Vector3 = Vector3(0, 0, 1)) -> tuple[List[Triangle], int]:
        # clipspace position and normal forms a plane.
        # anything further than the plane is cut out.
        d1 = signed_dist(point=self.vertex1, normal=clipspace_normal, plane_point=clipspace_pos)
        d2 = signed_dist(point=self.vertex2, normal=clipspace_normal, plane_point=clipspace_pos)
        d3 = signed_dist(point=self.vertex3, normal=clipspace_normal, plane_point=clipspace_pos)

        inside_points, outside_points = [], []
        for dist, vertex in zip([d1,d2,d3], [self.vertex1, self.vertex2, self.vertex3]):
            inside_points.append(vertex) if dist >= 0 else outside_points.append(vertex)

        if len(inside_points) == 0:
            clipped_triangles = []
            return clipped_triangles, len(inside_points)

        elif len(inside_points) == 3:
            clipped_triangles = [self]
            return clipped_triangles, len(inside_points)

        elif len(inside_points) == 1:
            # 1 inside point -> new triangle
            intersect_p1 = plane_line_intersectiion(clipspace_pos, clipspace_normal, inside_points[0], outside_points[0])
            intersect_p2 = plane_line_intersectiion(clipspace_pos, clipspace_normal, inside_points[0], outside_points[1])
            clipped_triangle = Triangle(v1=inside_points[0], v2=intersect_p1, v3=intersect_p2, color=self.color)
            clipped_triangles = [clipped_triangle]
            return clipped_triangles, len(inside_points)

        elif len(inside_points) == 2:
            # 1 outside point -> parallelogram -> split into two triangle
            intersect_p1 = plane_line_intersectiion(clipspace_pos, clipspace_normal, inside_points[0], outside_points[0])
            clipped_triangle1 = Triangle(v1=inside_points[0], v2=inside_points[1], v3=intersect_p1, color=self.color)
            intersect_p2 = plane_line_intersectiion(clipspace_pos, clipspace_normal, inside_points[1], outside_points[0])
            clipped_triangle2 = Triangle(v1=inside_points[1], v2=intersect_p2, v3=intersect_p1, color=self.color)
            clipped_triangles = [clipped_triangle1, clipped_triangle2]
            return clipped_triangles, len(inside_points)

    def update(self, screen, camera, light, world_position=Vector3(0, 0, 0), world_transform=Matrix.identity(), ):

        returns = []

        # local to world transform
        transformed: Triangle = self.transform(world_position, world_transform)
        world_triangle = copy.deepcopy(transformed)

        # determine visibility based on surface normal
        normal = transformed.get_normal_vec()
        angle = (camera.position - transformed.vertex1).dot(normal)
        show = angle > 0.0
        if show:
            # lighting
            transformed = light.shade(transformed, normal) if light is not None else transformed

            # view transform (map triangle into camera view)
            transformed = transformed.transform(transform_mat=camera.view_matrix)

            # clip triangles (cut out any triangle before camer near plane [too close to the camera])
            clipped_triangles, n_in = transformed.clip(clipspace_pos=Vector3(0,0,camera.near),
                                                       clipspace_normal=Vector3(0,0,1))

            for j, clipped_triangle in enumerate(clipped_triangles):

                # perspective tranform to clip space  x:-1~1, y:-1~1, z:0~1
                transformed = clipped_triangle.transform(transform_mat=camera.perspective_transform())

                if n_in == 3:
                    # for visualizing world coordinates
                    transformed.cache = world_triangle

                returns.append(transformed)
                # import draw
                # draw.draw_triangle_line(screen, transformed, color=(255,255,255))

        return returns

    def get_polygons(self):
        return [self.vertex1.get_xy(),
                self.vertex2.get_xy(),
                self.vertex3.get_xy(),]

    @classmethod
    def from_polygon_coord(self, polygon_coord, color=(255,255,255)):
        triangles = []
        for i in range(len(polygon_coord) + 1 - 3):
            indices = [0, i+1, i+2]
            vetrices = polygon_coord[indices]
            triangle = Triangle(v1=Vector3(array=vetrices[0][:3]),
                                v2=Vector3(array=vetrices[1][:3]),
                                v3=Vector3(array=vetrices[2][:3]), color=color)
            triangles.append(triangle)
        return triangles


    def __repr__(self):
        return f" Triangle: \n {self.vertex1} \n {self.vertex2} \n {self.vertex3}"
