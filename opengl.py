import sys, os
import numpy as np
import cv2
 
from PIL import Image
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
 
DISPLAY_WIDTH  = 800
DISPLAY_HEIGHT = 800
 
# 動画作成
fourcc = 0x00000021
fps = 30.0
video  = cv2.VideoWriter(os.path.join(os.path.dirname(__file__), 'output.mp4'), fourcc, fps, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
 
def load_texture():
    filepath = os.path.join(os.path.dirname(__file__), 'data/test.jpg')
    img = Image.open(filepath)
    w, h = img.size
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, img.tobytes())
 
def create_sphere(R, H0, K0, Z0, space):
    vertices = []
    for b in range(0,90,space):
        for a in range(0,360,space):
            vertex = [0, 0, 0, 0, 0]
            vertex[X] = R * np.sin((a) / 180 * np.pi) * np.sin((b) / 180 * np.pi) - H0
            vertex[Y] = R * np.cos((a) / 180 * np.pi) * np.sin((b) / 180 * np.pi) + K0
            vertex[Z] = R * np.cos((b) / 180 * np.pi) - Z0
            vertex[V] = (2 * b) / 360
            vertex[U] = (a) / 360
            vertices.extend([vertex])
 
            vertex = [0, 0, 0, 0, 0]
            vertex[X] = R * np.sin((a) / 180 * np.pi) * np.sin((b + space) / 180 * np.pi) - H0
            vertex[Y] = R * np.cos((a) / 180 * np.pi) * np.sin((b + space) / 180 * np.pi) + K0
            vertex[Z] = R * np.cos((b + space) / 180 * np.pi) - Z0
            vertex[V] = (2 * (b + space)) / 360
            vertex[U] = (a) / 360
            vertices.extend([vertex])
 
            vertex = [0, 0, 0, 0, 0]
            vertex[X] = R * np.sin((a + space) / 180 * np.pi) * np.sin((b) / 180 * np.pi) - H0
            vertex[Y] = R * np.cos((a + space) / 180 * np.pi) * np.sin((b) / 180 * np.pi) + K0
            vertex[Z] = R * np.cos((b) / 180 * np.pi) - Z0
            vertex[V] = (2 * b) / 360
            vertex[U] = (a + space) / 360
            vertices.extend([vertex])
 
            vertex = [0, 0, 0, 0, 0]
            vertex[X] = R * np.sin((a + space) / 180 * np.pi) * np.sin((b + space) / 180 * np.pi) - H0
            vertex[Y] = R * np.cos((a + space) / 180 * np.pi) * np.sin((b + space) / 180 * np.pi) + K0
            vertex[Z] = R * np.cos((b + space) / 180 * np.pi) - Z0
            vertex[V] = (2 * (b + space)) / 360
            vertex[U] = (a + space) / 360
            vertices.extend([vertex])
    return vertices
 
def resize(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(30.0, w/h, 1.0, 1000.0)
    glMatrixMode(GL_MODELVIEW)
 
def draw():
    global angleX, angleY
 
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
 
    glLoadIdentity()
    gluLookAt(3*R, 4*R, 5*R, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)
    glRotated(angleX, 1.0, 0.0, 0.0)
    glRotated(angleY, 0.0, 1.0, 0.0)
 
    glBindTexture(GL_TEXTURE_2D, tex)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
 
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(vertices_count):
        glTexCoord2f(vertices[i][U], vertices[i][V])
        glVertex3f(vertices[i][X], vertices[i][Y], -vertices[i][Z])
    for i in range(vertices_count):
        glTexCoord2f(vertices[i][U], -vertices[i][V])
        glVertex3f(vertices[i][X], vertices[i][Y], vertices[i][Z])
    glEnd()
 
    glFlush()
    glutSwapBuffers()
 
    image_buffer = glReadPixels(0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE)
    image = np.frombuffer(image_buffer, dtype=np.uint8).reshape(DISPLAY_WIDTH, DISPLAY_HEIGHT, 3)
    image = cv2.flip(image, 0)
    #cv2.imwrite(os.path.join(os.path.dirname(__file__), 'image.png'), image)
    video.write(image)
 
def keyboard(key, x, y):
    global angleX, angleY
    if key==b'q':
        video.release()
        sys.exit()
    elif key==b'h':
        angleY += 5.0
        glutPostRedisplay()
    elif key==b'j':
        angleX += 5.0
        glutPostRedisplay()
 
SPACE = 5
(R, H0, K0, Z0) = (100, 0, 0, 0)
(X, Y, Z, U, V) = (0, 1, 2, 3, 4)
vertices = create_sphere(R, H0, K0, Z0, SPACE)
vertices_count = len(vertices)#(90 / SPACE) * (360 / SPACE) * 4
angleX = 0.0
angleY = 0.0
 
glutInit(sys.argv)
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(DISPLAY_WIDTH, DISPLAY_HEIGHT)
glutCreateWindow(b"Sphere Test")
glutDisplayFunc(draw)
glutReshapeFunc(resize)
glutKeyboardFunc(keyboard)
 
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_BLEND)
glEnable(GL_TEXTURE_2D)
glClearColor(0.0, 0.0, 0.0, 0.0)
glEnable(GL_DEPTH_TEST)
 
tex = glGenTextures(1)
load_texture()
 
glutMainLoop()