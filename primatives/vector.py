from __future__ import annotations
from typing import Union
import numpy as np
import numbers

class Vector3():

    def __init__(self, x=0, y=0, z=0, array=None):
        self.w = 1
        if array is None:
            self.val = np.array([x, y, z], dtype=np.float32)
        else:
            self.val = array
            assert len(self.val) == 3
            assert self.val.ndim == 1

    @classmethod
    def zero(cls):
        return cls(x=0, y=0, z=0)

    @property
    def x(self):
        return self.val[0]

    @property
    def y(self):
        return self.val[1]

    @property
    def z(self):
        return self.val[2]

    def __add__(self, b: Union[Vector3, numbers.Number]):
        if isinstance(b, Vector3):
            new_val = self.val + b.val
        elif isinstance(b, numbers.Number):
            new_val = self.val + b
        else:
            raise ValueError('not a correct type')
        return Vector3(array=new_val)

    def __sub__(self, b):
        if isinstance(b, Vector3):
            new_val = self.val - b.val
        elif isinstance(b, numbers.Number):
            new_val = self.val - b
        else:
            raise ValueError('not a correct type')
        return Vector3(array=new_val)

    def __mul__(self, b):
        if isinstance(b, Vector3):
            new_val = self.val * b.val
        elif isinstance(b, numbers.Number):
            new_val = self.val * b
        else:
            raise ValueError('not a correct type')
        return Vector3(array=new_val)

    def __truediv__(self, b):
        if isinstance(b, Vector3):
            new_val = self.val / b.val
        elif isinstance(b, numbers.Number):
            new_val = self.val / b
        else:
            raise ValueError('not a correct type')
        return Vector3(array=new_val)

    def norm(self):
        return np.linalg.norm(self.val, ord=2, axis=-1)

    def normalize(self):
        mag = np.linalg.norm(self.val, ord=2, axis=-1)
        if mag == 0:
            val = Vector3.zero().val
        else:
            val = self.val / mag
        vec = Vector3(array=val)
        vec.w = self.w
        return vec

    def dot(self, b: Vector3):
        assert isinstance(b, Vector3)
        return np.dot(self.val, b.val)

    def cross_product(self, b: Vector3):
        assert isinstance(b, Vector3)
        new_val = np.cross(self.val, b.val)
        return Vector3(array=new_val)
        # x = self.y * b.z - self.z * b.y
        # y = self.z * b.x - self.x * b.z
        # z = self.x * b.y - self.y * b.x
        # return Vector3(x, y, z)

    def to_matrix(self):
        return np.array([[self.x, self.y, self.z, self.w]])

    def get_tuple(self):
        return (int(self.x), int(self.y))

    def __matmul__(self, other):
        from primatives.matrix import Matrix
        if not isinstance(other, Matrix):
            return NotImplemented
        output: Matrix = Matrix.from_vector(self) @ other
        return Vector3.from_matrix(output)

    @classmethod
    def from_matrix(self, matrix):
        from primatives.matrix import Matrix
        if not isinstance(matrix, Matrix):
            return NotImplemented
        assert matrix.row == 1
        assert matrix.col == 4
        val = matrix.val[0]
        w = val[3]
        if w != 0:
            vec = Vector3(x=val[0] / w, y=val[1] / w, z=val[2] / w)
        else:
            vec = Vector3(x=0, y=0, z=0)
        return vec

    def get_xy(self):
        return (int(self.x), int(self.y))

    def __repr__(self):
        return f" vec3: ({self.x}, {self.y}, {self.z})"
