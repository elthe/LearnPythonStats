#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
指定点函数。它们都以glVertex开头，后面跟一个数字和1~2个字母。例如：
glVertex2d
glVertex2f
glVertex3f
glVertex3fv
等等。
2代表的是二维坐标，3代表三维坐标
s表示16位整数（OpenGL中将这个类型定义为GLshort），
i表示32位整数（OpenGL中将这个类型定义为GLint和GLsizei），
f表示32位浮点数（OpenGL中将这个类型定义为GLfloat和GLclampf），
d表示64位浮点数（OpenGL中将这个类型定义为GLdouble和GLclampd）。
"""

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)


def drawFunc():
    glClear(GL_COLOR_BUFFER_BIT)

    # 分割线：这里我们没有指定颜色，所以使用OpenGL默认的颜色系统，即前景白色，背景黑色。
    glBegin(GL_LINES)
    glVertex2f(-1.0, 0.0)
    glVertex2f(1.0, 0.0)
    glVertex2f(0.0, 1.0)
    glVertex2f(0.0, -1.0)
    glEnd()

    # 指明每个点的大小为5个像素（否则默认是一个像素看不清楚，当然不是必要的）
    glPointSize(5.0)
    glBegin(GL_POINTS)

    # glColor3f(R, G, B)指定了绘制的颜色，这里的RGB都是0~1之间的浮点数
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(0.3, 0.3)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.6, 0.6)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(0.9, 0.9)
    glEnd()

    glColor3f(1.0, 1.0, 0)
    glBegin(GL_QUADS)
    glVertex2f(-0.2, 0.2)
    glVertex2f(-0.2, 0.5)
    glVertex2f(-0.5, 0.5)
    glVertex2f(-0.5, 0.2)
    glEnd()

    glColor3f(0.0, 1.0, 1.0)

    # glPolygonMode()指定了如何绘制面的方式，
    # GL_LINE为只画线，GL_FILL则是默认的填充。
    glPolygonMode(GL_FRONT, GL_LINE)
    glPolygonMode(GL_BACK, GL_FILL)

    glBegin(GL_POLYGON)
    glVertex2f(-0.5, -0.1)
    glVertex2f(-0.8, -0.3)
    glVertex2f(-0.8, -0.6)
    glVertex2f(-0.5, -0.8)
    glVertex2f(-0.2, -0.6)
    glVertex2f(-0.2, -0.3)
    glEnd()

    glPolygonMode(GL_FRONT, GL_FILL)
    glPolygonMode(GL_BACK, GL_LINE)
    glBegin(GL_POLYGON)
    glVertex2f(0.5, -0.1)
    glVertex2f(0.2, -0.3)
    glVertex2f(0.2, -0.6)
    glVertex2f(0.5, -0.8)
    glVertex2f(0.8, -0.6)
    glVertex2f(0.8, -0.3)
    glEnd()

    glFlush()


glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
glutInitWindowSize(400, 400)
glutCreateWindow("Sencond")

glutDisplayFunc(drawFunc)
init()
glutMainLoop()
