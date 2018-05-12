#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
【3D图像的最小单位，它们往往被称为图元】
点，在OpenGL中，这是最基本的图元，比如说图中红色的那个点。
线，比如左图中粉色的那根。我们可以看到，两个点定一条线，不过从一个点上可以发射出任意多的线，所以点和线的数量关系并不是确定的。
多边形，是最为复杂的图元，比如左图的黄色梯形。和数学中的多边形含义是一样的。


"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import gluLookAt, gluPerspective
from math import cos, sin, pi
from time import sleep
import sys

PI2 = pi * 2.0
WIN_X = 300
WIN_Y = 300
ANG = 0.0
ANGX = 0.0
theVortex = 0
winid = 0


def vortex(R=20.0, r=12.0):
    ''' Torus_Vortex '''
    nparts = 50
    mparts = 28
    detail = float(mparts) / float(nparts)
    tm = 0.0

    for m in range(mparts):
        m = float(m)
        c = float(m % 2)
        glColor3f(c * 0.5, c * 0.8, c * 1.0)

        # OpenGL所有的绘图指令，都必须包含在glBegin()和glEnd()之间
        # glBegin()的参数告诉OpenGL这些点最终的绘制方法
        # GL_POINTS 单个顶点集
        # GL_LINES 线段
        # GL_LINE_STRIP 不闭合的连续线段
        # GL_LINE_LOOP 闭合的线段
        # GL_POLYGON 多边形
        # GL_TRAINGLES 独立三角形
        # GL_TRAINGLE_STRIP 三角形串，线性连续
        # GL_TRAINGLE_FAN 三角形串，扇状连续
        # GL_QUADS 独立四边形
        # GL_QUAD_STRIP 四边形串
        glBegin(GL_QUAD_STRIP)

        move = 0.0
        for n in range(nparts + 1):
            n = float(n)
            move += detail
            x = r * cos(n / nparts * PI2)
            y = r * sin(n / nparts * PI2)
            for o in (0.0, 1.0):
                tm = o + m + move;
                mx = (x + R) * cos(tm / mparts * PI2)
                mz = (x + R) * sin(tm / mparts * PI2)
                glVertex3f(mx, y, mz)
        glEnd()


def init():
    global theVortex
    glClearColor(0.0, 0.0, 0.0, 0.0)

    # 开启深度测试
    glEnable(GL_DEPTH_TEST)

    theVortex = glGenLists(1)

    # 说明一个显示列表的开始，其后的OpenGL函数存入显示列表中，直至调用结束表的函数（见下面）。
    # 参数list是一个正整数，它标志唯一的显示列表。
    # 参数mode的可能值有GL_COMPILE和GL_COMPILE_AND_EXECUTE。
    # 若要使后面的函数语句只存入而不执行，则用GL_COMPILE；
    # 若要使后面的函数语句存入表中且按瞬时方式执行一次，则用GL_COMPILE_AND_EXECUTE。
    glNewList(theVortex, GL_COMPILE)

    vortex(18.0, 12.0)

    # 标志显示列表的结束。
    glEndList()


def display():
    """
    绘制回调函数
    :return:
    """
    global theVortex
    glClearColor(0.0, 0.0, 0.0, 0.0)

    # 是把先前的画面给清除，这基本是定律，每次重绘之前都要把原来的画面擦除，否则叠加起来什么都看不出了。
    # glClear一看就知道是OpenGL原生的命令，而参数就是指明要清除的buffer。
    # 清除颜色缓冲区时，清除深度缓冲区
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # 当你做了一些移动或旋转等变换后，使用glPushMatrix();OpenGL 会把这个变换后的位置和角度保存起来。
    # 然后你再随便做第二次移动或旋转变换，再用glPopMatrix();OpenGL 就把刚刚保存的那个位置和角度恢复。
    glPushMatrix()

    # 简单来说四个参数第一个是角度，后三个是一个向量，意义就是绕着这个向量旋转，这里是绕着Y轴旋转1°。
    glRotatef(ANGX, 1.0, 0.0, 0.0)
    glRotatef(ANG, 0.0, -1.0, 0.0)

    glCallList(theVortex)

    # 就把刚刚保存的那个位置和角度恢复。
    glPopMatrix()
    glutSwapBuffers()


def idle():
    global ANG
    ANG += 1.0
    sleep(0.01)

    # glutPostRedisplay函数会标记当前窗体来重新显示,它会促使主循环尽快的调用完显示函数.
    # 注意它只影响当前窗体(获得焦点的窗体),不是所有窗体.
    glutPostRedisplay()


def reshape(Width, Height):
    """
    调整窗口大小回调函数
    :param Width:
    :param Height:
    :return:
    """
    far = 30.0

    if (Width == Height):
        glViewport(0, 0, Width, Height)
    elif (Width > Height):
        glViewport(0, 0, Height, Height)
    else:
        glViewport(0, 0, Width, Width)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # glFrustum(-10.0,10.0,-10.0,10.0,3.0,60.0)
    gluPerspective(80.0, 1.0, 1.0, 80.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0.0, 0.0, far, 0.0, 0.0, 0.0, 0.0, 1.0, far)


def hitkey(key, mousex, mousey):
    global winid, ANGX
    if (str(key) == 'q'):
        # 关闭窗体和它包含的子窗体
        glutDestroyWindow(winid)
        # 退出软件
        sys.exit()
    elif (str(key) == 'a'):
        ANGX += 1.0


def main():
    global WIN_X, WIN_Y, winid

    # glutInit是用glut来初始化OpenGL的，所有的问题都交给这个函数吧，
    # 基本不用管，虽说可以接受参数的，基本无用。
    glutInit(sys.argv)

    # glutInitDisplayMode(MODE)非常重要，这里告诉系统我们需要一个怎样显示模式。
    # 至于其参数GLUT_RGBA就是使用(red, green, blue)的颜色系统。
    # 有没有写错？这里有个A啊，不应该是(red, green, blue, alpha)么？
    # 大概是历史原因，GLUT_RGBA和GLUT_RGB是其实是等价的（坑爹啊），要想实现Alpha还得用其他的参数。
    # 而GLUT_SINGLE意味着所有的绘图操作都直接在显示的窗口执行，
    # 相对的，我们还有一个双缓冲的窗口，对于动画来说非常合适。
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH)

    # 这个函数很容易理解，设置出现的窗口的大小。
    glutInitWindowSize(400, 400)
    glutInitWindowSize(WIN_X, WIN_Y)

    # 也很常用，用来设置窗口出现的位置。
    glutInitWindowPosition(100, 100)

    # 一旦调用了，就出现一个窗口了，参数就是窗口的标题。
    winid = glutCreateWindow("Vortex")

    init()

    # 是glut非常讨人喜欢的一个功能，它注册了一个函数，用来绘制OpenGL窗口，
    # 这个函数里就写着很多OpenGL的绘图操作等命令，也就是我们主要要学习的东西。
    glutDisplayFunc(display)

    # 又是一个激动人心的函数，可以让OpenGL在闲暇之余，
    # 调用一下注册的函数，这是是产生动画的绝好方法。
    glutIdleFunc(idle)

    glutReshapeFunc(reshape)
    glutKeyboardFunc(hitkey)

    # 主循环，一旦调用了，我们的OpenGL就一直运行下去了。
    # 和很多程序中的主循环一样，不停的运行，画出即时的图像，处理输入等。
    glutMainLoop()


if __name__ == "__main__":
    main()
