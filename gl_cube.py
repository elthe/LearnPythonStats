#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
OpenGL with PyOpenGL introduction and creation of Rotating Cube
"""

import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from common import openglcm

verticies = (
    (1, 1, -1),  # A1
    (1, -1, -1),  # B1
    (-1, -1, -1),  # C1
    (-1, 1, -1),  # D1

    (1, 1, 1),  # A2
    (1, -1, 1),  # B2
    (-1, -1, 1),  # C2
    (-1, 1, 1)  # D2
)

edges = (
    (0, 1),  # A1-B1
    (1, 2),  # B1-C1
    (2, 3),  # C1-D1
    (0, 3),  # A1-D1

    (0, 4),  # A1-A2
    (1, 5),  # B1-B2
    (2, 6),  # C1-C2a
    (3, 7),  # D1-D2

    (4, 5),  # A2-B2
    (5, 6),  # B2-C2
    (6, 7),  # C2-D2
    (4, 7)  # A2-D2
)

surfaces = (
    (0, 1, 2, 3),  # A1-B1-C1-D1
    (4, 5, 6, 7),  # A2-B2-C2-D2
    (0, 1, 5, 4),  # A1-B1-B2-A2
    # (1, 2, 6, 5),  # B1-C1-C2-B2
    # (2, 3, 7, 6),  # C1-D1-D2-C2
    # (0, 3, 7, 4)  # A1-D1-D2-A2
)

surface_color = (
    (1.0, 0.0, 0.0),  # red
    (1.0, 1.0, 1.0),  # white
    (0.0, 1.0, 0.0),  # green
    (1.0, 0.0, 1.0),  # magenta
    (1.0, 1.0, 0.0),  # yellow
    (0.0, 1.0, 1.0)  # cyan
)


def Cube():
    # 绘制Cube各个顶点
    glPointSize(5.0)
    glBegin(GL_POINTS)
    glColor3f(1.0, 1.0, 0.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

    # 绘制Cube各条棱边
    glLineWidth(9.0)
    glEnable(GL_LINE_SMOOTH)
    glBegin(GL_LINES)
    glColor3f(0.0, 1.0, 0.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

    # GL_QUADS 独立四边形
    glPolygonMode(GL_FRONT, GL_FILL)
    glPolygonMode(GL_BACK, GL_FILL)
    glBegin(GL_QUADS)
    for i in range(len(surfaces)):
        surface = surfaces[i]
        red, green, blue = surface_color[i]
        glColor3f(red, green, blue)
        for vertex in surface:
            glVertex3fv(verticies[vertex])
    glEnd()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)

    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 旋转
        glRotatef(1, 3, 1, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)


main()
