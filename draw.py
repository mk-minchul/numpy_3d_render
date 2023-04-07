import colorsys
import copy

import pygame
from composite.point import Point
from primatives.vector import Vector3
from primatives.matrix import Matrix
from typing import List
from composite.triangle import Triangle
from transformations import from_pygame_to_clip_space
from ops import quick_inverse
import numpy as np
import constants
from transformations import to_pygame_space


def hsv2rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))


def rgb2hsv(r, g, b):
    tuple(round(i * 255) for i in colorsys.rgb_to_hsv(r / 255., g / 255., b / 255.))


def draw_axis(screen, camera, length=3, draw_point=True, stroke=5):
    center = Point(Vector3(0, 0, 0))
    x = Point(Vector3(length, 0, 0), color=(255, 0, 0))
    y = Point(Vector3(0, length, 0), color=(0, 255, 0))
    z = Point(Vector3(0, 0, length), color=(0, 0, 255))

    origin = center.update(screen=screen,
                           world_position=Vector3(0, 0, 0),
                           world_transform=Matrix.identity(),
                           camera=camera, draw_point=draw_point)

    x_axis = x.update(screen=screen,
                      world_position=Vector3(0, 0, 0),
                      world_transform=Matrix.identity(),
                      camera=camera, draw_point=draw_point)
    y_axis = y.update(screen=screen,
                      world_position=Vector3(0, 0, 0),
                      world_transform=Matrix.identity(),
                      camera=camera, draw_point=draw_point)
    z_axis = z.update(screen=screen,
                      world_position=Vector3(0, 0, 0),
                      world_transform=Matrix.identity(),
                      camera=camera, draw_point=draw_point)

    pygame.draw.line(screen, x_axis.color, origin.position.get_xy(), x_axis.position.get_xy(), stroke)
    pygame.draw.line(screen, y_axis.color, origin.position.get_xy(), y_axis.position.get_xy(), stroke)
    pygame.draw.line(screen, z_axis.color, origin.position.get_xy(), z_axis.position.get_xy(), stroke)
    fontsize = 20
    font = pygame.font.SysFont('mono', fontsize)
    screen.blit(font.render('xaxis', True, x_axis.color), x_axis.position.get_xy())
    screen.blit(font.render('yaxis', True, y_axis.color), y_axis.position.get_xy())
    screen.blit(font.render('zaxis', True, z_axis.color), z_axis.position.get_xy())

    vmat = quick_inverse(camera.view_matrix).val
    screen.blit(font.render('view matrix', True, (255,255,255)), (0, 0))
    screen.blit(font.render(f'{["{}{:.2f}".format(" "  if v >= -0.00001 else "-", np.abs(v) ) % v for v in vmat[0]]}', True, (255,0,0)), (0, fontsize))
    screen.blit(font.render(f'{["{}{:.2f}".format(" "  if v >= -0.00001 else "-", np.abs(v)) % v for v in vmat[1]]}', True, (0,255,0)), (0, fontsize*2))
    screen.blit(font.render(f'{["{}{:.2f}".format(" "  if v >= -0.00001 else "-", np.abs(v)) % v for v in vmat[2]]}', True, (0,0,255)), (0, fontsize*3))
    screen.blit(font.render(f'{["{}{:.2f}".format(" "  if v >= -0.00001 else "-", np.abs(v)) % v for v in vmat[3]]}', True, (255,255,255)), (0, fontsize*4))

    screen.blit(font.render(f'yaw: {camera.yaw:.2f} pitch: {camera.pitch:.2f}', True, (255,0,0)), (0, fontsize*5))


def draw_triangle_line(screen, triangle, color=(255, 255, 255)):

    pygame.draw.line(screen, color, triangle.vertex1.get_xy(), triangle.vertex2.get_xy(), 1)
    pygame.draw.line(screen, color, triangle.vertex2.get_xy(), triangle.vertex3.get_xy(), 1)
    pygame.draw.line(screen, color, triangle.vertex3.get_xy(), triangle.vertex1.get_xy(), 1)


def draw_triangles(screen,
                   triangles: List[Triangle],
                   draw_fill: bool = True,
                   draw_wireframe: bool = True,
                   draw_text: bool = True):
    for triangle in triangles:
        draw_triangle(screen, triangle, draw_fill=draw_fill, draw_wireframe=draw_wireframe)


def draw_triangle(screen,
                  triangle: Triangle,
                  draw_fill: bool = True,
                  draw_wireframe: bool = True,
                  draw_text: bool = True):

    # transform to pygame space
    pg_triange = copy.deepcopy(triangle)
    pg_triange.vertex1 = to_pygame_space(triangle.vertex1)
    pg_triange.vertex2 = to_pygame_space(triangle.vertex2)
    pg_triange.vertex3 = to_pygame_space(triangle.vertex3)

    if draw_fill:
        pygame.draw.polygon(screen, pg_triange.color, pg_triange.get_polygons())
    if draw_wireframe:
        draw_triangle_line(screen, pg_triange, (255,255,255))
    if draw_text:
        fontsize = 20
        font = pygame.font.SysFont('timesnewroman', fontsize)
        for i, point in enumerate(pg_triange.get_polygons()):
            # clip coordinate render
            clip_point = from_pygame_to_clip_space(point)
            text = font.render(f'({clip_point[0]:.2f}, {clip_point[1]:.2f})', True, (0, 255, 0))
            screen.blit(text, point)
            if hasattr(pg_triange, 'cache'):
                world_point = getattr(pg_triange.cache, f'vertex{i+1}')
                # world coordinate render
                text = font.render(f'({world_point.val[0]:.2f}, {world_point.val[1]:.2f}, {world_point.val[2]:.2f})', True, (0, 0, 255))
                screen.blit(text, (point[0], point[1]-fontsize))


def draw_all_minimaps(screen, world, camera,):
    minimap_size = max(constants.Width // 5, constants.Height // 5)

    # x, y
    loc_top = constants.Width - minimap_size
    loc_left = constants.Height - minimap_size
    draw_minimap(screen, world, camera, minimap_size, loc_top, loc_left, axis=[0,1])

    # x, z
    loc_top = constants.Width - minimap_size
    loc_left = constants.Height - 2 * minimap_size
    draw_minimap(screen, world, camera, minimap_size, loc_top, loc_left, axis=[0,2])

    # z, y
    loc_top = constants.Width - minimap_size
    loc_left = constants.Height - 3 * minimap_size
    draw_minimap(screen, world, camera, minimap_size, loc_top, loc_left, axis=[2,1])

def draw_minimap(screen, world, camera, minimap_size, loc_top, loc_left, axis=[0,1]):

    pygame.draw.rect(screen, (200,200,200), pygame.Rect(loc_left, loc_top, minimap_size, minimap_size))

    # maps range to 0,1
    x_val = camera.position.val[axis[0]]    # -4 - 4
    if axis[0] == 1:
        x_val = x_val * -1
    if axis[0] == 2:
        x_val = x_val * -1
    xmin, xmax = -4, 4
    x_val = (x_val - xmin) / (xmax-xmin)    #  0 - 1
    camera_x = unnormalize(x_val, minimap_size, loc_left)

    y_val = camera.position.val[axis[1]]    # -4 - 4
    if axis[1] == 1:
        y_val = y_val * -1
    if axis[1] == 2:
        y_val = y_val * -1
    ymin, ymax = -4, 4
    y_val = (y_val - ymin) / (ymax-ymin)    #  0 - 1
    camera_y = unnormalize(y_val, minimap_size, loc_top)

    pygame.draw.circle(screen, (255,255,255), (camera_x, camera_y), radius=10)




def unnormalize(x, scale, offset):
    return (x * scale + offset)