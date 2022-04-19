from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time
import threading
from modules.draw import*
from modules.gameobject import GameObject
from modules.textures import loadTexture
from modules.transforms import *



#---------------------OBJETOS QUE CAEN------------------------#
def objetosCaen():
    vive = 2
    coord_aparicion = 0.0
    while vive>=1:
        nueva_coord =  (float)(random.randint(-1, 1))
        if(nueva_coord > coord_aparicion+0.1 or nueva_coord < coord_aparicion-0.1):
            coord_aparicion = nueva_coord
            draw_objeto(coord_aparicion,0,0.05,32,1,1,1)
            countdown(3)
            vive = vive-1

def countdown(num_of_secs):
    while num_of_secs:
        m, s = divmod(num_of_secs, 60)
        min_sec_format = '{:02d}:{:02d}'.format(m, s)
        print(min_sec_format, end='/r')
        time.sleep(1)
        num_of_secs -= 1

def draw_objeto(xc,yc,R,n,c1,c2,c3):
    angle = 2*3.141592/n
    glColor3f(c1,c2,c3)
    glBegin(GL_POLYGON)
    for i in range(n):
        x = xc + R*np.cos(angle*i)
        y = yc + R*np.sin(angle*i)
        glVertex2d(x,y)
    glEnd()


