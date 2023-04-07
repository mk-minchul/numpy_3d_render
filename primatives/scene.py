from typing import List, Optional
from composite.mesh.mesh_base import Mesh
from primatives.camera import Camera
from primatives.matrix import Matrix
from primatives.vector import Vector3
import ops
from composite.triangle import Triangle
import draw
from ops import z_sort


class Scene():

    def __init__(self, camera: Camera, world: List[Mesh], omni_camera: Optional[Camera] = None):
        self.camera = camera
        self.world: List[Mesh] = world
        for obj in self.world:
            assert isinstance(obj, Mesh)
        self.omni_camera = omni_camera

    def add_object(self, object: Mesh):
        assert isinstance(object, Mesh)
        self.world.append(object)

    def update_scene(self, screen, light, use_omni_cam=False, draw_fill=True, draw_wireframe=True, draw_text=True):
        # temporary
        # self.camera.yaw = 0.2
        # self.camera.position = Vector3(0.1, 0.1, 0.1)
        # self.camera.pitch = 0.9

        if use_omni_cam:
            camera = self.omni_camera
        else:
            camera = self.camera

        triangles = self.get_triangles_from_world(screen, self.world, camera, light)

        # draw triangles
        draw.draw_triangles(screen, triangles, draw_fill=draw_fill, draw_wireframe=draw_wireframe, draw_text=draw_text)

        # draw axis
        draw.draw_axis(screen, camera, length=3)

        # draw minimap
        # draw.draw_all_minimaps(screen, self.world, self.camera)
        if use_omni_cam:
            # world coord
            planes = self.camera.get_frustum_planes_in_world_coord()
            triangles = [triangle for plane in planes for triangle in Triangle.from_polygon_coord(plane)]
            triangles = [tri for triangle in triangles for tri in triangle.update(screen, self.omni_camera, light=None)]
            draw.draw_triangles(screen, triangles, draw_fill=False, draw_wireframe=True, draw_text=False)

    def get_triangles_from_world(self, screen, world: List[Mesh], camera, light):

        triangles = []
        for mesh in world:
            updated_mesh = mesh.update(screen, camera, light)
            triangles.extend(updated_mesh)

        triangles.sort(key=z_sort)
        return triangles
