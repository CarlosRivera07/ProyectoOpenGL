from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.draw import *
from modules.transforms import *
from modules.textures import loadTexture
from modules.bezier import evaluate_bezier
from modules.gameobject import GameObject
import random
#from playsound import playsound #Instalar con pip install playsound==1.2.2
from threading import Thread
from movimientoObj import *


#--------------------DECLARACION DE VARIABLES GLOBALES------------------------#

w,h= 500,750

vidas = 1

#Texturas
texture_fondo = []
texture_canasta = []
texture_balon = []
counter_elements = 0

#ELEMENTOS DE LA CANASTA
canasta_gameobject = GameObject()

#Movimiento
flag_left = False
flag_right = False

#--------------------------------------------------------------------------#



#-----------------------------DIBUJOS TEXTURAS-----------------------------#
#FONDO
def draw_fondo():
    global texture_fondo

    x_coord = 0
    y_coord = 0
    width = 500
    height = 650
    glBindTexture(GL_TEXTURE_2D, texture_fondo[0])
    glBegin(GL_POLYGON)
    glTexCoord2f(0,0)
    glVertex2d(x_coord,y_coord)
    glTexCoord2f(1,0)
    glVertex2d(x_coord + width,y_coord)
    glTexCoord2f(1,1)
    glVertex2d(x_coord + width,y_coord + height)
    glTexCoord2f(0,1)
    glVertex2d(x_coord,y_coord + height)
    glEnd()

#CANASTA
def draw_canasta():
    global canasta_gameobject
    x,y = canasta_gameobject.get_position()
    w,h = canasta_gameobject.get_size()
    pin_x_start, pin_x_end = (1,0) if canasta_gameobject.is_mirrored() else (0,1)
    glBindTexture(GL_TEXTURE_2D, canasta_gameobject.get_frame_to_draw())
    glBegin(GL_POLYGON)
    glTexCoord2f(pin_x_start,0)
    glVertex2d(x,y)
    glTexCoord2f(pin_x_end,0)
    glVertex2d(x+w,y)
    glTexCoord2f(pin_x_end,1)
    glVertex2d(x+w,y+h)
    glTexCoord2f(pin_x_start,1)
    glVertex2d(x,y+h)
    glEnd()

#BALON


#----------------------------------------------------------------------#

#---------------------EVENTOS DEL TECLADO------------------------------#

def keyPressed ( key, x, y):
    global flag_left, flag_right
    if key == b'\x1b':
        glutLeaveMainLoop()
    if key == b'a' or key == b'A':
        flag_left = True
    if key == b'd' or key == b'D':
        flag_right = True

def keyUp(key, x, y):
    global flag_left, flag_right
    if key == b'a' or key == b'A':
        flag_left = False
    if key == b'd' or key == b'D':
        flag_right = False

#---------------------------------------------------------------------------#


def init():
    glClearColor ( 0.5725, 0.5647, 1.0, 0.0 )
    glEnable(GL_TEXTURE_2D)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

def reshape(width, height):
    global w, h
    glViewport ( 0, 0, width, height )
    glMatrixMode ( GL_PROJECTION )
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    w = width
    h = height
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

def display():
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

    #----------------------------DIBUJAR AQUI---------------------------------#
    
    #DIBUJO DE LAS TEXTURAS
    draw_fondo()
    draw_canasta()

    coord_aparicion = 0.0
    while vidas == 1:
        nueva_coord =  (float)(random.randint(-1, 1))
        if(nueva_coord > coord_aparicion+0.1 or nueva_coord < coord_aparicion-0.1 or coord_aparicion == 0.0):
            coord_aparicion = nueva_coord
            objetoCae(coord_aparicion)
            

    
    
    #----------------------------------------------------------------------------#

    glutSwapBuffers()

def animate():
    temp = 0
    #global xc_circle, yc_circle, radius, w, h

#-------------------------------TIMERS-------------------------------------------#
def timer_move_canasta(value):
    global canasta_gameobject, flag_left, flag_right
    state = canasta_gameobject.get_state()
    input = {'x': 0, 'y': 0}
    src_w = w
    if flag_right:
        input['x'] = 1
    elif flag_left:
        input['x'] = -1
    canasta_gameobject.move(input, src_w)

    velocity = canasta_gameobject.get_velocity()

    glutPostRedisplay()
    glutTimerFunc(20, timer_move_canasta, 1)

def timer_animate_canasta(value):
    global canasta_gameobject
    canasta_gameobject.animate()
    glutPostRedisplay()
    glutTimerFunc(100, timer_animate_canasta,1)

#--------------------------------------------------------------------------------#


def main():
    global texture_canasta, canasta_gameobject, counter_elements
    glutInit (  )
    glutInitDisplayMode ( GLUT_RGBA )
    glutInitWindowSize ( w, h )
    glutInitWindowPosition(500,0)
    
    glutCreateWindow( "BasCLER" )
    glutDisplayFunc (display)
    #glutIdleFunc ( animate )
    glutReshapeFunc ( reshape )
    glutKeyboardFunc( keyPressed )
    glutKeyboardUpFunc(keyUp)
    init()

    #--------------------------------CARGAR TEXTURAS--------------------------------------#
    #Canasta
    texture_canasta.append([loadTexture('Resources/canastabuena.png')])
    canasta_gameobject = GameObject(counter_elements,190,50,120,100, texture_canasta)
    counter_elements += 1

    #Balon
    texture_balon.append(loadTexture(''))

    #Elementos del Fondo
    texture_fondo.append(loadTexture('Resources/fondo.png'))


    timer_move_canasta(0)
    timer_animate_canasta(0)

    glutMainLoop()

print("Presiona Escape para cerrar.")
main()