from primatives.vector import Vector3
from primatives.matrix import Matrix
import numpy as np
from constants import ASPECT_RATIO
import ops


class Camera():
    def __init__(self,
                 position: Vector3,
                 near: float,
                 far: float,
                 fov: float,
                 yaw: float = 0.0,
                 pitch: float = 0.0):
        self.position = position
        self.near = near
        self.far = far
        self.fov = fov  # in degree
        self.yaw = yaw
        self.pitch = pitch

        self.world_default_view_direction = Vector3(0, 0, -1)  # looking into -z direction
        self.world_default_up = Vector3(0, 1, 0)
        self.speed = 1.0

    def perspective_transform(self):
        # https://www.notion.so/Perspective-Transform-15120ef620124e649543072e8bc0e9c1
        # intrinsic matrix
        fov_radian = self.fov / 180. * np.pi
        tangent = np.tan(fov_radian / 2)
        f = self.far
        n = self.near

        # z is being mapped to 0 (near) and 1 (far)
        # x and y are being mapped such that the boundary of FOV becomes 1 at each depth.
        projection_mat = np.array([
            [ASPECT_RATIO / tangent, 0, 0, 0],
            [0, 1 / tangent, 0, 0],
            [0, 0, f / (f - n), 1],
            [0, 0, -f * n / (f - n), 0],
        ])
        return Matrix(array=projection_mat)

    @property
    def view_matrix(self):
        rotationy = Matrix.rotation_y(self.yaw)
        rotationx = Matrix.rotation_x(self.pitch)
        rotation = rotationx @ rotationy
        camera_view_direction = self.world_default_view_direction @ rotation
        camera_back_direction = camera_view_direction * -1
        camera_back_target = self.position + camera_back_direction
        up = self.position + self.world_default_up @ rotationx @ rotationy
        view_matrix = ops.view_matrix(self.position, camera_back_target, up)
        return view_matrix

    @property
    def view_direction(self):
        rotationy = Matrix.rotation_y(self.yaw)
        rotationx = Matrix.rotation_x(self.pitch)
        rotation = rotationx @ rotationy
        camera_view_direction = self.world_default_view_direction @ rotation
        return camera_view_direction

    def get_frustum_planes_in_world_coord(self):
        # get frustum planes in camera coordinates
        fov_radian = self.fov / 180. * np.pi

        x_near = np.tan(fov_radian / 2) * self.near
        y_near = ASPECT_RATIO * np.tan(fov_radian / 2) * self.near
        near = np.array([
            (x_near, y_near, self.near, 1),
            (x_near, -y_near, self.near, 1),
            (-x_near, -y_near, self.near, 1),
            (-x_near, y_near, self.near, 1),
        ])

        x_far = np.tan(fov_radian / 2) * self.far
        y_far = ASPECT_RATIO * np.tan(fov_radian / 2) * self.far
        far = np.array([
            (x_far, y_far, self.far, 1),
            (x_far, -y_far, self.far, 1),
            (-x_far, -y_far, self.far, 1),
            (-x_far, y_far, self.far, 1),
        ])

        top = np.array([
            (-x_near, y_near, self.near, 1),
            (x_near, y_near, self.near, 1),
            (x_far, y_far, self.far, 1),
            (-x_far, y_far, self.far, 1),
        ])

        bottom = np.array([
            (-x_near, -y_near, self.near, 1),
            (x_near, -y_near, self.near, 1),
            (x_far, -y_far, self.far, 1),
            (-x_far, -y_far, self.far, 1),
        ])

        left = np.array([
            (-x_near, -y_near, self.near, 1),
            (-x_near, y_near, self.near, 1),
            (-x_far, y_far, self.far, 1),
            (-x_far, -y_far, self.far, 1),
        ])

        right = np.array([
            (x_near, -y_near, self.near, 1),
            (x_near, y_near, self.near, 1),
            (x_far, y_far, self.far, 1),
            (x_far, -y_far, self.far, 1),
        ])


        # convert to world coordinates
        inv_view_mat = ops.quick_inverse(self.view_matrix).val
        near = near @ inv_view_mat
        far = far @ inv_view_mat
        top = top @ inv_view_mat
        bottom = bottom @ inv_view_mat
        left = left @ inv_view_mat
        right = right @ inv_view_mat
        return near, far, top, bottom, left, right
