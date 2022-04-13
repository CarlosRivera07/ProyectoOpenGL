from tkinter import CENTER
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from modules.draw import*
from modules.transforms import *


#---------------------IMPORTACIONES------------------------#

from bloque import *

#---------------------VARIABLES GLOBALES------------------------#

w = 500
h = 650

xc_circle = 250
yc_circle = 250
radius = 25

x1 = -0.15
y1 = -0.9
x2 = 0.15
y2 = -0.85
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


    
    
def display():
    global x1, x2, y1, y2
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    #glMatrixMode ( GL_MODELVIEW )
    #glLoadIdentity()

    #---------------------DIBUJAR AQUI------------------------#
    #glRectf(-0.8, -0.8, 0.5, 0.5)

            # ANCHO = 500  ALTO = 650
            # ALTO = 650

    #Rectangulo principal
    
    glColor3f(1,1,1) #Colores del rectangulo
    glRectf(x1,y1,x2,y2) #Coordenadas del rectangulo
    
    #Resto de rectangulos
    #Fila 1
    bloqueF1_1()
    bloqueF1_2()
    bloqueF1_3()
    bloqueF1_4()
    bloqueF1_5()
    #Fila 2
    bloqueF2_1()
    bloqueF2_2()
    bloqueF2_3()
    bloqueF2_4()
    bloqueF2_5()
    #Fila 3
    bloqueF3_1()
    bloqueF3_2()
    bloqueF3_3()
    bloqueF3_4()
    bloqueF3_5()
    #Fila 4
    bloqueF4_1()
    bloqueF4_2()
    bloqueF4_3()
    bloqueF4_4()
    bloqueF4_5()
    #Fila 5
    bloqueF5_1()
    bloqueF5_2()
    bloqueF5_3()
    bloqueF5_4()
    bloqueF5_5()
    #Fila 6
    bloqueF6_1()
    bloqueF6_2()
    bloqueF6_3()
    bloqueF6_4()
    bloqueF6_5()
    #Fila 7
    bloqueF7_1()
    bloqueF7_2()
    bloqueF7_3()
    bloqueF7_4()
    bloqueF7_5()
    #---------------------------------------------------------#

    glFlush()
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
    global w,h
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
    
    glutMainLoop()

print("Presiona Escape para cerrar.")
main()