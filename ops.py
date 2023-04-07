from primatives.matrix import Matrix
from primatives.vector import Vector3
import numpy as np


def quick_inverse(m):
    matrix = Matrix()
    matrix.val[0][0], matrix.val[0][1], matrix.val[0][2], matrix.val[0][3] = m.val[0][0], m.val[1][0], m.val[2][0], 0.0
    matrix.val[1][0], matrix.val[1][1], matrix.val[1][2], matrix.val[1][3] = m.val[0][1], m.val[1][1], m.val[2][1], 0.0
    matrix.val[2][0], matrix.val[2][1], matrix.val[2][2], matrix.val[2][3] = m.val[0][2], m.val[1][2], m.val[2][2], 0.0
    matrix.val[3][0] = -(
                m.val[3][0] * matrix.val[0][0] + m.val[3][1] * matrix.val[1][0] + m.val[3][2] * matrix.val[2][0])
    matrix.val[3][1] = -(
                m.val[3][0] * matrix.val[0][1] + m.val[3][1] * matrix.val[1][1] + m.val[3][2] * matrix.val[2][1])
    matrix.val[3][2] = -(
                m.val[3][0] * matrix.val[0][2] + m.val[3][1] * matrix.val[1][2] + m.val[3][2] * matrix.val[2][2])
    matrix.val[3][3] = 1.0
    return matrix


def view_matrix(current: Vector3, target: Vector3, up: Vector3) -> Matrix:
    '''
    Extrinsic Matrix
    view matrix is created by inverted a look at matirx.
    look at matrix is a transformation of axis from camera to the world.
    So it is created by putting 3 world axis right, up and forward in world matrix as 4x4 matrix.
    '''
    z_axis0 = (target - current).normalize()  # makes z axis start from origin as we have translation in 4x4 matrix
    true_up = (up - current).normalize()     # makes y axis start from origin as we have translation in 4x4 matrix
    right = true_up.cross_product(z_axis0).normalize()

    val = [
        [right.x,   right.y,   right.z,   0.0],
        [true_up.x, true_up.y, true_up.z, 0.0],
        [z_axis0.x, z_axis0.y, z_axis0.z, 0.0],
        [current.x, current.y, current.z, 1.0],
    ]
    mat = Matrix(array=np.array(val))
    view_mat = quick_inverse(mat)

    # forward here is -target, so it is negative
    # Create the view matrix in row vector notation
    # view_matrix = np.array([[right.x, up.x, -forward.x, 0],
    #                         [right.y, up.y, -forward.y, 0],
    #                         [right.z, up.z, -forward.z, 0],
    #                         [-np.dot(right.val, current.val), -np.dot(up.val, current.val), np.dot(forward.val, current.val), 1]])
    return view_mat


def signed_dist(point: Vector3, normal: Vector3, plane_point: Vector3, normal_is_normalized: bool = True):
    # we assume normal is normalized
    if normal_is_normalized:
        return (point - plane_point).dot(normal)
    else:
        return (point - plane_point).dot(normal) / normal.norm()


def plane_line_intersectiion(plane_point: Vector3,
                             normal: Vector3,
                             line_start: Vector3,
                             line_end: Vector3,
                             normal_is_normalized: bool = True):
    if not normal_is_normalized:
        normal = normal.normalize()
    diff = line_end - line_start
    # for intersection to be on the plane : normal * intersection = normal * plane_point
    # intersection = line_start + t * (line_end-line_start)
    # substitute in and solve for t
    # https://www.youtube.com/watch?v=e8Ftm7HSy6I
    t = (normal.dot(plane_point) - normal.dot(line_start)) / normal.dot(diff)
    intersection = line_start + (diff * t)
    return intersection


def z_sort(val):
    # val is a triangle
    return -(val.vertex1.val[2] + val.vertex2.val[2] + val.vertex3.val[2]) / 3.0
