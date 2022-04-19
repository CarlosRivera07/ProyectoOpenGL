import threading
#from turtle import width
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.draw import*
from modules.gameobject import GameObject
from modules.textures import loadTexture
#from modules.bezier import evaluate_bezier
from modules.transforms import *
import random
from threading import Thread



#---------------------IMPORTACIONES------------------------#

#from movimientoObj import *
import random
#---------------------VARIABLES GLOBALES------------------------#

w = 500
h = 650

#DECLARACION DE TEXTURAS
texture_logo = []


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
    if key == b'w' :
        flag_up = False
    if key == b's':
        flag_down = False
    if key == b'a':
        flag_left = False
    if key == b'd':
        flag_right = False

#---------------------------------------------------------#

def init():
    glClearColor ( 0.0, 0.0, 0.0, 0.0 )
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

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

#DIBUJAR CIRCULO
def polygon(xc,yc,R,n,c1,c2,c3):
    angle = 2*3.141592/n
    glColor3f(c1,c2,c3)
    glBegin(GL_POLYGON)
    for i in range(n):
        x = xc + R*np.cos(angle*i)
        y = yc + R*np.sin(angle*i)
        glVertex2d(x,y)
    glEnd()

    #DIBUJAR TEXTURA DE LA CANASTA
def draw_logo():
    global texture_logo
    x_coord = -0.1
    y_coord = -0.1
    widthv = 0.2
    heightv = 0.2
    glBindTexture(GL_TEXTURE_2D, texture_logo[0])
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex2d(x_coord,y_coord)
    glTexCoord2f(1,0)
    glVertex2d(x_coord + widthv,y_coord)
    glTexCoord2f(1,1)
    glVertex2d(x_coord + widthv,y_coord + heightv)
    glTexCoord2f(0,1)
    glVertex2d(x_coord,y_coord + heightv)
    glEnd()

def display():
    global x1, x2, y1, y2
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

    #---------------------DIBUJAR AQUI------------------------#
     

    #FONDO DEGRADADO
    glBegin(GL_QUADS)
    glColor3f(0.2,0,0.1)
    glVertex2d(-1,-1)
    glColor3f(0,0,1)
    glVertex2d(1,-1)
    glColor3f(1,0.2,0)
    glVertex2d(1,1)
    glColor3f(1,.5,0)
    glVertex2d(-1,1)
    glEnd()

    #BARRA DE REBOTE
    
    glColor3f(1,1,1) #Colores del rectangulo
    glRectf(x1,y1,x2,y2) #Coordenadas del rectangulo
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
    elif(x1 <= -1 and flag_left): #Si llega al borde izquiferdo
        x1 = -1
        x2 = -1+largo
        
    
    if flag_left or flag_right or flag_up or flag_down:
        glutPostRedisplay()

def main():
    global w,h, texture_logo, largo, ancho 
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
    #texture_fondo.append(loadTexture('Resources/fondo.png'))
    texture_logo.append(loadTexture('Resources/clerback2.png'))

    glutMainLoop()

print("Presiona Escape para cerrar.")
main()