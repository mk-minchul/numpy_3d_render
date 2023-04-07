from typing import Optional
import pygame
from primatives.camera import Camera

def handle_event(camera: Camera, dt: float, omni_camera: Optional[Camera]):
    running = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    camera_event_handler(camera, dt)

    use_omni_cam = omni_camera_handler(omni_camera)
    return running, use_omni_cam

def camera_event_handler(camera: Camera, dt: float):
    keys = pygame.key.get_pressed()
    delta = camera.speed * dt
    if keys[pygame.K_UP]:
        camera.position.val[1] = camera.position.val[1] + delta
    if keys[pygame.K_DOWN]:
        camera.position.val[1] = camera.position.val[1] - delta
    if keys[pygame.K_RIGHT]:
        camera.position.val[0] = camera.position.val[0] + delta
    if keys[pygame.K_LEFT]:
        camera.position.val[0] = camera.position.val[0] - delta

    if keys[pygame.K_w]: #zoom in
        # camera.position.val = camera.position.val + delta
        camera.pitch -= 0.04
    if keys[pygame.K_s]: #zoom out
        # camera.position.val = camera.position.val - delta
        camera.pitch += 0.04
    if keys[pygame.K_a]:
        camera.yaw -= 0.04
    if keys[pygame.K_d]:
        camera.yaw += 0.04

    if keys[pygame.K_1]: #zoom in
        camera.position.val = camera.position.val - (camera.view_direction * delta).val
    if keys[pygame.K_2]: #zoom out
        camera.position.val = camera.position.val + (camera.view_direction * delta).val


def omni_camera_handler(omni_camera: Optional[Camera]):
    if omni_camera is None:
        return False
    if not hasattr(omni_camera, 'use_omni_cam'):
        omni_camera.use_omni_cam = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_o]:
        return not omni_camera.use_omni_cam
    return omni_camera.use_omni_cam