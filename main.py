import pygame
from constants import SIZE, DOUBLEBUF, BACKGROUND_COLOR, FPS
from primatives.vector import Vector3
from primatives.camera import Camera
from primatives.scene import Scene
from composite.mesh.mesh_base import Mesh
from composite.mesh.cube import get_cube_triangles
from light.directional import DirectionalLight
import event
import numpy as np

pygame.init()
screen = pygame.display.set_mode(size=SIZE, flags=DOUBLEBUF, depth=16)
clock = pygame.time.Clock()

pygame.mouse.get_rel()
pygame.mouse.set_visible(True)
pygame.event.set_grab(False)


if __name__ == '__main__':
    cube_triangles = get_cube_triangles(color=(240, 84, 84), position=Vector3(0, 0, 5), scale=1)
    cube = Mesh(triangles=cube_triangles, position=Vector3(0, 0, 0))
    cubes = [cube]

    # create camera
    camera = Camera(position=Vector3(0, 0, -6), near=0.1, far=1000, fov=75)
    omni_camera = Camera(position=Vector3(2000, 0, 0), near=0.1, far=1000, fov=75, yaw=-np.pi/3)

    # make light
    light = DirectionalLight(position=Vector3(0.9, 0.9, -1))

    # create scene and the world
    scene = Scene(camera=camera, world=cubes, omni_camera=omni_camera)

    yaw_delta = np.radians(0.5)
    pitch_delta = np.radians(1.0)
    frame_count = 0

    run = True
    while run:

        screen.fill(BACKGROUND_COLOR)  # resets the screen

        clock.tick(FPS)
        dt = clock.tick(FPS) / 100
        frame_rate = clock.get_fps()
        pygame.display.set_caption(str(frame_rate) + " fps")
        run, use_omni_cam = event.handle_event(camera, dt, omni_camera)
        # display scene
        scene.update_scene(screen, light=light, use_omni_cam=use_omni_cam)
        pygame.display.flip()

        # change camera angle for next frame
        if camera.yaw > np.pi/4 and yaw_delta > 0:
            yaw_delta = -yaw_delta
        if camera.yaw < -np.pi/4 and yaw_delta < 0:
            yaw_delta = -yaw_delta
        camera.yaw += yaw_delta
        if camera.pitch > np.pi/6 and pitch_delta > 0:
            pitch_delta = -pitch_delta
        if camera.pitch < -np.pi/6 and pitch_delta < 0:
            pitch_delta = -pitch_delta
        camera.pitch += pitch_delta
        frame_count += 1


