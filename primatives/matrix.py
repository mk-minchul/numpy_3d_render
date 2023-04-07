from __future__ import annotations
import numpy as np
from primatives.vector import Vector3
from math import cos, sin


class Matrix():

    """Represents a matrix with standard operation support."""

    def __init__(self, r: int = 4, c: int = 4, array=None):
        """Initialize new Matrix with r rows and c cols. Sets all values to 0.0."""
        if array is None:
            self.val = np.zeros((r, c), dtype=np.float32)
        else:
            self.val = array
            assert self.val.ndim == 2

    def __repr__(self) -> str:
        """repr(self)"""
        return f"matrix: \n{self.val}"

    @property
    def row(self) -> int:
        """The number of rows in self."""
        return len(self.val)

    @property
    def col(self) -> int:
        """The number of cols in self."""
        return len(self.val[0])

    @classmethod
    def from_vector(cls, vec: Vector3) -> Matrix:
        """Construct a new Matrix formed by a Vector3.
        Returns:
            Matrix - matrix with size 1, 4 populated by vec's x, y, z, w.
        """
        val = np.array([[vec.x, vec.y, vec.z, vec.w]])
        return Matrix(array=val)

    @classmethod
    def rotation_x(cls, angle: float) -> Matrix:
        """Construct a matrix which performs a rotation around the x-axis by angle radians
        Arguments:
            angle - angle in radians to for xrotmat to represent.
        Returns:
            Matrix - angle rotation around x-axis Matrix
        """
        val = [
            [1, 0.0, 0.0, 0.0],
            [0.0, cos(angle), sin(angle), 0.0],
            [0.0, -sin(angle), cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return Matrix(array=np.array(val, dtype=np.float32))

    @classmethod
    def rotation_y(cls, angle: float) -> Matrix:
        """Construct a matrix which performs a rotation around the y-axis by angle radians
        Arguments:
            angle - angle in radians to for yrotmat to represent.
        Returns:
            Matrix - angle rotation around y-axis Matrix
        """
        val = [
            [cos(angle), 0.0, -sin(angle), 0.0],
            [0.0, 1, 0.0, 0.0],
            [sin(angle), 0.0, cos(angle), 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return Matrix(array=np.array(val, dtype=np.float32))

    @classmethod
    def rotation_z(cls, angle: float) -> Matrix:
        """Construct a matrix which performs a rotation around the z-axis by angle radians
        Arguments:
            angle - angle in radians to for zrotmat to represent.
        Returns:
            Matrix - angle rotation around z-axis Matrix
        """
        val = [
            [cos(angle),  sin(angle), 0.0, 0.0],
            [-sin(angle), cos(angle), 0.0, 0.0],
            [0.0,         0.0,        1,   0.0],
            [0.0,         0.0,        0.0, 1],
        ]
        return Matrix(array=np.array(val, dtype=np.float32))

    @classmethod
    def scaling(cls, scale: float) -> Matrix:
        """Construct a scaling matrix for the given scale factor.
        Arguments:
            scale - float, the scale value for Matrix to be constructed for
        Returns:
            Matrix - the scaling Matrix
        """
        val = [
            [scale, 0.0, 0.0, 0.0],
            [0.0, scale, 0.0, 0.0],
            [0.0, 0.0, scale, 0.0],
            [0.0, 0.0, 0.0, 1],
        ]
        return Matrix(array=np.array(val, dtype=np.float32))

    @classmethod
    def identity(cls, size: int = 4) -> Matrix:
        """Construct an identity matrix of the given size. Defined as a square matrix
        with 1s on the main diagonal, and 0s elsewhere.
        Arguments:
            size - int, the size of the identity matrix.
        Returns:
            Matrix - the specified identity matrix.
        """
        return Matrix(array=np.eye(size, dtype=np.float32))

    @classmethod
    def translate(cls, position: Vector3) -> Matrix:
        """Construct a Matrix that performs a translation specified by the give
        position.
        Arguments:
            position - the Vector3 to construct translation matrix by.
        Returns:
            Matrix - the constructed translation Matrix.
        """
        val = [
            [1, 0.0, 0.0, position.x],
            [0.0, 1, 0.0, position.y],
            [0.0, 0.0, 1, position.z],
            [0.0, 0.0, 0.0, 1],
        ]
        return Matrix(array=np.array(val, dtype=np.float32))

    def __matmul__(self, other: Matrix) -> Matrix:
        """Support for self @ other, defined as matrix multiplication.
        Raises:
            ValueError - if self and other have incompatible dimensions.
        Returns:
            Matrix - product of self and other, size is self.row x other.col.
        """
        if not isinstance(other, Matrix):
            return NotImplemented

        if self.col != other.row:
            raise ValueError(
                "Matrices incompatible for multiplication, got: "
                f"{(self.row, self.col)}, {(other.row, other.col)}"
            )

        val = self.val @ other.val
        return Matrix(array=val)

    def transpose(self) -> Matrix:
        """Compute the transpose of self. Defined as the matrix formed by swapping the
        rows and cols of self.
        Returns:
            Matrix - transpose of self.
        """
        return Matrix(array=self.val.T)

    def submatrix(self, row: int, col: int) -> Matrix:
        """Form the matrix resulting from removing the specified row and col
        from self.
        Returns:
            Matrix - self without row or col.
        """
        val = np.delete(self.val, row, axis=0)
        val = np.delete(val, col, axis=1)
        return Matrix(array=val)

    def det(self) -> float:
        """Calculate the determinant of self.
        Raises:
            ValueError - If self is not square.
        Returns:
            float - self's determinant.
        """

        if self.row != self.col:
            raise ValueError("Matrix determinant only defined for square matrices.")

        if self.row == 2:
            return self.val[0][0] * self.val[1][1] - self.val[0][1] * self.val[1][0]
        return np.linalg.det(self.val)

