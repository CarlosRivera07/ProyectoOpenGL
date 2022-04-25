from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from modules.draw import *
from modules.transforms import *
from modules.textures import loadTexture
from modules.bezier import evaluate_bezier
from modules.gameobject import GameObject
import random
from threading import Thread
from movimientoObj import objetoCae


#--------------------DECLARACION DE VARIABLES GLOBALES------------------------#

w,h= 500,650

vidas = 3
puntos = 0

#Texturas
texture_fondo = []
texture_canasta = []
texture_balon = []
texture_bomba = []
texture_logo = []
counter_elements = 0
balones = []
bombas = []

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

#Logo
def draw_logo():
    global texture_logo

    x_coord = 215
    y_coord = 315
    width = 75
    height = 75
    glBindTexture(GL_TEXTURE_2D, texture_logo[0])
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

#CANASTA - DEGRADADO
def draw_canasta():
    global canasta_gameobject
    x,y = canasta_gameobject.get_position()
    w,h = canasta_gameobject.get_size()
    pin_x_start, pin_x_end = (1,0) if canasta_gameobject.is_mirrored() else (0,1)
    glBindTexture(GL_TEXTURE_2D, canasta_gameobject.get_frame_to_draw())
    glBegin(GL_POLYGON)
    glTexCoord2f(pin_x_start,0)
    glColor3f(0,0,0)
    glVertex2d(x,y)
    glTexCoord2f(pin_x_end,0)
    glColor3f(1,0,0)
    glVertex2d(x+w,y)
    glTexCoord2f(pin_x_end,1)
    glColor3f(1,1,1)
    glVertex2d(x+w,y+h)
    glTexCoord2f(pin_x_start,1)
    glColor3f(0,0,1)
    glVertex2d(x,y+h)
    glEnd()

#BALON
def draw_balones():
    if vidas != 0:
        global balones
        for i in range(len(balones)):
            balon_gameobject = balones[i]
            x,y = balon_gameobject.get_position()
            w,h = balon_gameobject.get_size()
            pin_x_start, pin_x_end = (0,1)
            glBindTexture(GL_TEXTURE_2D, texture_balon[0])
            glBegin(GL_POLYGON)
            glTexCoord2f(pin_x_start,0)
            glColor3f(1,1,1)
            glVertex2d(x,y)
            glTexCoord2f(pin_x_end,0)
            glColor3f(1,1,1)
            glVertex2d(x+w,y)
            glTexCoord2f(pin_x_end,1)
            glColor3f(1,1,1)
            glVertex2d(x+w,y+h)
            glTexCoord2f(pin_x_start,1)
            glColor3f(1,1,1)
            glVertex2d(x,y+h)
            glEnd()

def draw_bomba():
    if vidas != 0:
        global texture_bomba, bombas
        for i in range(len(bombas)):
            bomba_gameobject = bombas[i]
            x,y = bomba_gameobject.get_position()
            w,h = bomba_gameobject.get_size()
            pin_x_start, pin_x_end = (0,1)
            glBindTexture(GL_TEXTURE_2D, texture_bomba[0])
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

#----------------------------------------------------------------------#

#COLISIONES
def check_collisions():
    global bombas, canasta_gameobject, balones, vidas, puntos
    for i in range(len(bombas)):
        if canasta_gameobject.is_collision(bombas[i]):
            if vidas != 0:
                vidas = vidas-1
                print("Vidas restantes: "+str(vidas))
                bombas.pop(i)
            return
    for i in range(len(balones)):
        if canasta_gameobject.is_collision(balones[i]):
            puntos = puntos+1
            print("Puntos: "+str(puntos))
            balones.pop(i)
            return

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
    global vidas
    glClear ( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glMatrixMode ( GL_MODELVIEW )
    glLoadIdentity()

#----------------------------DIBUJAR AQUI---------------------------------#
    
    #DIBUJO DE LAS TEXTURAS
    draw_fondo()
    draw_logo()
    draw_canasta()
    draw_balones()
    draw_bomba()

    glutSwapBuffers()

#----------------------------------------------------------------------------#

def animate():
    temp = 0

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

    check_collisions()
    glutPostRedisplay()
    glutTimerFunc(20, timer_move_canasta, 1)

def timer_animate_canasta(value):
    global canasta_gameobject
    glutPostRedisplay()
    glutTimerFunc(100, timer_animate_canasta,1)

def timer_move_balon(id_balon):
    global balones, w
    for i in range(len(balones)):
        if balones[i].get_id() == id_balon:
            balones[i].static_move(balones,w)
            glutPostRedisplay()
            glutTimerFunc(20, timer_move_balon, id_balon)

def timer_animate_balon(id_balon):
    global balones
    for i in range(len(balones)):
        if balones[i].get_id() == id_balon:
            #balones[i].animate()
            glutPostRedisplay()
            glutTimerFunc(200, timer_animate_balon, id_balon)

def timer_create_balon(value):
    global balones, texture_balon, counter_elements
    id_balon = counter_elements
    balon = GameObject(id_balon,(float)(random.randint(40, 430)),610,40,40, texture_balon)
    counter_elements += 1
    balones.append(balon)
    #glutPostRedisplay()
    timer_animate_balon(id_balon)
    timer_move_balon(id_balon)
    glutTimerFunc(1800, timer_create_balon, 1)

def timer_move_bomba(id_bomba):
    global bombas, w
    for i in range(len(bombas)):
        if bombas[i].get_id() == id_bomba:
            bombas[i].static_move(bombas,w)
            glutPostRedisplay()
            glutTimerFunc(20, timer_move_bomba, id_bomba)

def timer_animate_bombas(id_bomba):
    global bombas
    for i in range(len(bombas)):
        if bombas[i].get_id() == id_bomba:
            glutPostRedisplay()
            glutTimerFunc(200, timer_animate_bombas, id_bomba)
            
def timer_create_bombas(value):
    global bombas, texture_bomba, counter_elements
    id_bomba = counter_elements
    bomba = GameObject(id_bomba,(float)(random.randint(40, 430)),610,40,40, texture_bomba)
    counter_elements += 1
    bombas.append(bomba)
    #glutPostRedisplay()
    timer_animate_bombas(id_bomba)
    timer_move_bomba(id_bomba)
    glutTimerFunc(3000, timer_create_bombas, 1)

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
    texture_balon.append(loadTexture('Resources/balon.png'))

    #Bomba
    texture_bomba.append(loadTexture('Resources/bomba.png'))

    #Elementos del Fondo
    texture_fondo.append(loadTexture('Resources/fondo.png'))
    texture_logo.append(loadTexture('Resources/clerback2.png'))


    timer_move_canasta(0)
    timer_animate_canasta(0)
    timer_create_balon(0)
    timer_create_bombas(0)

    glutMainLoop()

print("Presiona Escape para cerrar.")
main()