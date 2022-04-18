from tkinter import CENTER
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from modules.draw import*
from modules.gameobject import GameObject
from modules.textures import loadTexture
from modules.transforms import *


#---------------------IMPORTACIONES------------------------#

from bloque import *
import random
#---------------------VARIABLES GLOBALES------------------------#

w = 500
h = 650

#DECLARACION DE TEXTURAS
texture_canasta = []


#Elementos de la canasta

radius = 0.015
xc_circle = 0
yc_circle = -0.8 - (radius*2)

x1 = -0.15
y1 = -0.9
x2 = 0.15
y2 = -0.85
ancho = 0.05
largo = 0.3
velocidad = 0.002

flag_left = False
flag_right = False
flag_up = False
flag_down = False

input = 0

#---------------------FUNCIONES DEL TECLADO------------------------#

def keyPressed ( key, x, y ):
    global flag_left, flag_right, flag_up, flag_down
    if key == b'\x1b':
        glutLeaveMainLoop()
    if key == b'w':
        flag_up = True
    if key == b's':
        flag_down = True
    if key == b'a':
        flag_left = True
    if key == b'd':
        flag_right = True

def keyUp(key, x, y):
    global flag_left, flag_right, flag_up, flag_down
    if key == b'w':
        flag_up = False
    if key == b's':
        flag_down = False
    if key == b'a':
        flag_left = False
    if key == b'd':
        flag_right = False

def init():
    glClearColor ( 0.0, 0.0, 0.0, 0.0 )

def reshape(width, height):
    global w,h
    glViewport ( 0, 0, width, height )
    glMatrixMode ( GL_PROJECTION )
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    w = width
    h = height
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

def polygon(xc,yc,R,n,c1,c2,c3):
    angle = 2*3.141592/n
    glColor3f(c1,c2,c3)
    glBegin(GL_POLYGON)
    for i in range(n):
        x = xc + R*np.cos(angle*i)
        y = yc + R*np.sin(angle*i)
        glVertex2d(x,y)
    glEnd()

    #DIBUJAR CANASTA
def draw_canasta():
    global x1,x2,y1,y2,ancho,largo,texture_canasta
    glEnable(GL_TEXTURE_2D);
    glBindTexture(GL_TEXTURE_2D, texture_canasta[0])
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex2d(x1,y1)
    glTexCoord2f(0,1)
    glVertex2d(x1,y2)
    glTexCoord2f(1,1)
    glVertex2d(x2,y2)
    glTexCoord2f(1,0)
    glVertex2d(x2,y1)
    glEnd()

    #DIBUJAR FIGURAS
def draw_figura(xc,yc,R,n,c1,c2,c3):
    angle = 2*3.141592/n
    glColor3f(c1,c2,c3)
    glBegin(GL_POLYGON)
    for i in range(n):
        x = xc + R*np.cos(angle*i)
        y = yc + R*np.sin(angle*i)
        glVertex2d(x,y)
    glEnd()

def display():
    global x1, x2, y1, y2
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

    #---------------------DIBUJAR AQUI------------------------#
     
    vive = 1

    while vive==1:
        coord_aparicion = (float)(random.randint(-1, 1))
        #llamar a la funcion de crear objeto enviandole la coordenada de X (coordenada Y siempre es -1)
        draw_figura(coord_aparicion,-1,0.1,32,1,1,1)
        vive = 0
    

            # ANCHO = 500  ALTO = 650
            # ALTO = 650

    #BARRA DE REBOTE
    
    #glColor3f(1,1,1) #Colores del rectangulo
    #glRectf(x1,y1,x2,y2) #Coordenadas del rectangulo

    draw_canasta()

    #---------------------------------------------------------#

    
    glutSwapBuffers()

def animate():
    global x1, y1, x2, y2, w, h
    global flag_left, flag_right, flag_up, flag_down

    input = 0
    if flag_right:
        input = 1
    elif flag_left:
        input = -1
    else:
        input = 0


    if(input == 0): #no se esta presionando nada
        x1 = x1
        x2 = x2
    elif(input == 1): #Se esta presionando a la derecha
        print("d")
        #Derecha
        if(x2 <= 1):
            x1 = x1 + velocidad
            x2 = x2 + velocidad
        else:
            x1 = x1
            x2 = x2

    elif(input == -1): #Se esta presionando a la izquierda
        print("a")
        #Izquierda
        if(x1 >= -1):
            x1 = x1 - velocidad
            x2 = x2 - velocidad
        else:
            x1 = x1
            x2 = x2

    #limites para la pantalla

    if(x2 >= 1 and flag_right): #Si llega al borde derecho
        x2 = 1
        x1 = 1-largo
    elif(x1 <= -1 and flag_left): #Si llega al borde izquierdo
        x1 = -1
        x2 = -1+largo
        
    
    if flag_left or flag_right or flag_up or flag_down:
        glutPostRedisplay()

    


def main():
    global w,h, texture_canasta, largo, ancho 
    glutInit (  )
    glutInitDisplayMode ( GLUT_RGBA )
    glutInitWindowSize ( w, h )
    glutInitWindowPosition(500,50)
    
    glutCreateWindow( "Jueguito chido" )
    glutDisplayFunc (display)
    glutIdleFunc ( animate )
    #glutReshapeFunc ( reshape )
    glutKeyboardFunc( keyPressed )
    glutKeyboardUpFunc(keyUp)
    init()

    #CARGAR TEXTURAS
    
    texture_canasta.append([loadTexture('Resources/canasta.png')])
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, largo, ancho, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_canasta)

    glutMainLoop()

print("Presiona Escape para cerrar.")
main()