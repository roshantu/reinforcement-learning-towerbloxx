#coding=utf-8

from UIObject import UIObject
from UI import *
from Constants import *
import math

class UITower(object):
    DECREASE_HEIGHT = 25
    
    def __init__(self, name):
        self.floors = []
        self.falling_floor = None
        self.max_floor_count = 3
        self.factor = 0.0
        self.state_height = 0
        
    def count_floor_to_show(self, floor_count):
        self.max_floor_count = floor_count
        
    def append_floor(self, ui_object):
        if self.falling_floor == None:
            self.falling_floor = ui_object
        else:
            raise Exception("No se puede agregar un nuevo piso y todavia esta descendiendo el anterior")
    
    def finished_dropping(self):
        return self.falling_floor == None
        
    def start(self, state):
        pass

    def set_state(self, state):
        self.factor= state.tower.factor
        self.state_height = state.tower.height

        height = len(self.floors)
        if height > 0:
            last_floor = self.floors[height -1]
            last_floor.rectangle.left = self.get_x_axis(state.tower.position, last_floor.get_width())
            self._move_floors_snake_like()

    def draw(self, screen):
        if not self.falling_floor == None:
            self._move_falling_floor()
            
            floor = self.falling_floor
            if self._has_stopped_falling():
                self._set_y_axis_floor(floor)
                if self._must_add_new_floor():
                   self.floors.append(floor)
                else:
                    screen.blit(floor.surface, floor.rectangle)                
                self.falling_floor = None

        #hay que dibujar los ultimos n pisos...
        last_n_floors = self._get_placed_last_n_floors()
        for floor in last_n_floors:
            screen.blit(floor.surface, floor.rectangle)

    def _must_add_new_floor(self):
        return len(self.floors) < self.state_height

    def _move_floors_snake_like(self): #no quiero pensar mas nombre de metodos
        height = len(self.floors)
        if height > 2: #si hay al menos tres pisos, quiero posicionar todos los del medio
            index = height - 1
            while index > 2:
                upper_floor = self.floors[index]
                middle_floor = self.floors[index-1]
                down_floor = self.floors[index-2]

                #MALISIMA CUENTA, DE FISICA CERO CHE...
                move_percentaje = self.factor * (index-1) / height
                move_percentaje = abs(move_percentaje)

                sgn_move=1
                if upper_floor.rectangle.left < down_floor.rectangle.left:
                    sgn_move = -1

                space_to_move = abs(upper_floor.rectangle.left - down_floor.rectangle.left)

                middle_floor.rectangle.left += math.ceil(move_percentaje * space_to_move * sgn_move)
                index -=1

    def _set_y_axis_floor(self, floor):
        height = len(self.floors)
        if height == 0:
            floor.rectangle.bottom = SCREEN_HEIGHT
        else:
            last_floor = self.floors[height-1]
            floor.rectangle.bottom = last_floor.rectangle.top + 1


    def _get_placed_last_n_floors(self):
        floor_count = len(self.floors)
        invisible_floor_count = floor_count - self.max_floor_count
        if invisible_floor_count > 0:
            last_floors = []            
            for i in range(invisible_floor_count, floor_count):
                last_floors.append(self.floors[i])
            self._place_bottom_screen(last_floors)
            return last_floors
        else:
            return self.floors
            
    def _place_bottom_screen(self, floors):
        y_axis = SCREEN_HEIGHT
        for floor in floors:
            floor.rectangle.bottom = y_axis
            y_axis -= floor.get_height() - 1

    def _has_stopped_falling(self):
        falling_floor = self.falling_floor
        if self._must_add_new_floor() and len(self.floors)>0:
            last_floor = self.floors[len(self.floors)-1]
            return falling_floor.rectangle.bottom >= (last_floor.rectangle.bottom - 1)
        else:
            return falling_floor.rectangle.bottom >= SCREEN_HEIGHT

    def _move_falling_floor(self):
        decrease_height = UITower.DECREASE_HEIGHT
        floor = self.falling_floor
        floor.move_horizontally(decrease_height)
   
    def get_x_axis(self, position, ui_width):
        shifted_position = position + 50
        buckets = SCREEN_WIDTH / 99 #posiciones en total 
        
        x_axis = buckets * shifted_position
        x_axis = x_axis - (ui_width/2) #lo centra
        return x_axis

        
