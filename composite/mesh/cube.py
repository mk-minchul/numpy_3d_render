from composite.triangle import Triangle
from primatives.vector import Vector3


def get_cube_triangles(color=(240,84,84), position=Vector3(), scale=1):
    return [
        Triangle(Vector3(-1.0, -1.0, -1.0) * scale + position, Vector3(-1.0, 1.0, -1.0) * scale + position,
                 Vector3(1.0, 1.0, -1.0) * scale + position, color),
        Triangle(Vector3(-1.0, -1.0, -1.0) * scale + position, Vector3(1.0, 1.0, -1.0) * scale + position,
                 Vector3(1.0, -1.0, -1.0) * scale + position, color),

        Triangle(Vector3(1.0, -1.0, -1.0) * scale + position, Vector3(1.0, 1.0, -1.0) * scale + position,
                 Vector3(1.0, 1.0, 1.0) * scale + position, color),
        Triangle(Vector3(1.0, -1.0, -1.0) * scale + position, Vector3(1.0, 1.0, 1.0) * scale + position,
                 Vector3(1.0, -1.0, 1.0) * scale + position, color),

        Triangle(Vector3(1.0, -1.0, 1.0) * scale + position, Vector3(1.0, 1.0, 1.0) * scale + position,
                 Vector3(-1.0, 1.0, 1.0) * scale + position, color),
        Triangle(Vector3(1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, 1.0, 1.0) * scale + position,
                 Vector3(-1.0, -1.0, 1.0) * scale + position, color),

        Triangle(Vector3(-1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, 1.0, 1.0) * scale + position,
                 Vector3(-1.0, 1.0, -1.0) * scale + position, color),
        Triangle(Vector3(-1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, 1.0, -1.0) * scale + position,
                 Vector3(-1.0, -1.0, -1.0) * scale + position, color),

        Triangle(Vector3(-1.0, 1.0, -1.0) * scale + position, Vector3(-1.0, 1.0, 1.0) * scale + position,
                 Vector3(1.0, 1.0, 1.0) * scale + position, color),
        Triangle(Vector3(-1.0, 1.0, -1.0) * scale + position, Vector3(1.0, 1.0, 1.0) * scale + position,
                 Vector3(1.0, 1.0, -1.0) * scale + position, color),

        Triangle(Vector3(1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, -1.0, 1.0) * scale + position,
                 Vector3(-1.0, -1.0, -1.0) * scale + position, color),
        Triangle(Vector3(1.0, -1.0, 1.0) * scale + position, Vector3(-1.0, -1.0, -1.0) * scale + position,
                 Vector3(1.0, -1.0, -1.0) * scale + position, color),
    ]
