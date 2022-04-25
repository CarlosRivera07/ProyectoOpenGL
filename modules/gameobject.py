class GameObject:
    """Clase para objectos como Mario y Goomba"""
    
    def __init__(self, id_element=0,x=0, y=0, w=0, h=0, frames = []):
        self.__position = {'x': 0, 'y': 0}
        self.__last_position = {'x': 0, 'y': 0}
        self.__size = {'x': 0, 'y': 0}
        self.animator = [] #Lista bidimensional con los Frames del objeto
        self.__index_state = 0 #Indice del estado del personaje a animar
        self.__latest_frame = 0 #Indice del frame a dibujar
        self.__mirror = False #mirror es False cuando voltea hacia la derecha
        self.__velocity = {'x': 0, 'y': 0}
        self.__MAX_VELOCITY = 8
        
        self.__id_element = id_element
        self.__position['x'] = x
        self.__position['y'] = y
        self.__last_position['x'] = x
        self.__last_position['y'] = y
        self.__size['x'] = w
        self.__size['y'] = h
        self.animator = frames

    def static_move(self, boxes, scr_w):
        if self.__velocity['y'] == 0:
            self.__velocity['y'] = 1
        
        self.__position['y'] -= self.__velocity['y'] * 2


    def move(self, input, src_w):
        #input['x']:
        #1.- Mover hacia la derecha
        #0.- No se mueve
        #-1.- Mover hacia la izquierda

        if  input['y'] == 1:
            self.__velocity['y'] = self.__MAX_VELOCITY

        #SI NO SE MUEVE
        if input['x'] == 0:
            if self.__velocity['x'] != 0:
                self.__velocity['x'] -= 0.9*self.__velocity['x']
            if abs(self.__velocity['x']) < 0.9:
                self.__velocity['x'] = 0 
        else:
            #SI SE ESTA MOVIENDO, YA SEA IZQUIERDA O DERECHA
            self.__velocity['x'] = self.__position['x'] - self.__last_position['x'] + input['x']
            if self.__velocity['x'] > self.__MAX_VELOCITY:
                self.__velocity['x'] = self.__MAX_VELOCITY
            if self.__velocity['x'] < -self.__MAX_VELOCITY:
                self.__velocity['x'] = -self.__MAX_VELOCITY

        self.__last_position['x'] = self.__position['x']
        self.__position['x'] += self.__velocity['x']

        if self.__position['x'] + self.__size['x'] > src_w:
            self.__position['x'] = src_w - self.__size['x']
            self.__velocity['x'] *= -1
        if self.__position['x']  < 0:
            self.__position['x'] = 0
            self.__velocity['x'] *= -1

    def is_collision(self,obj):
        if not isinstance(obj, GameObject):
            raise Exception('La función requiere un GameObject')
        col_x = self.__position['x'] + (self.__size['x'] / 2) - 10 < obj.__position['x'] + obj.__size['x'] and self.__position['x'] + (self.__size['x'] / 2) + 10 > obj.__position['x']
        col_y = self.__position['y'] + (self.__size['y'] / 4) < obj.__position['y'] + obj.__size['y'] and self.__position['y'] + (self.__size['y'] / 4) > obj.__position['y']
        return col_x and col_y

    def change_state(self, index):
        if index >= len(self.animator):
            raise Exception('El índice está fuera del límite permitido.')
        self.__index_state = index
        self.__latest_frame = 0
    
    def get_state(self):
        return self.__index_state

    def animate(self):
        if len(self.animator[self.__index_state]) == 1:
            return
        self.__latest_frame = 0 if self.__latest_frame >= (len(self.animator[self.__index_state]) - 1) else self.__latest_frame + 1

    def get_frame_to_draw(self):
        return self.animator[self.__index_state][self.__latest_frame]
    
    def get_position(self):
        return self.__position['x'], self.__position['y']

    def set_position(self, pos):
        self.__position = pos
    
    def get_size(self):
        return self.__size['x'], self.__size['y']

    def set_mirror(self, value):
        self.__mirror = value

    def is_mirrored(self):
        return self.__mirror
    
    def get_id(self):
        return self.__id_element
    
    def get_velocity(self):
        return self.__velocity