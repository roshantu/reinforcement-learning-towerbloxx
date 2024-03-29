#coding=utf-8

from UIObject import UIObject
from Constants import * 

class UICounter(object):
    MARGIN = 10

    def __init__(self, name):
        zero = COUNTER_PATH + "0" + IMAGE_EXTENSION
        images = [zero, zero, zero]
        self.ui_objects = []
        for img in images:
            self.ui_objects.append(UIObject(name, img))

    def start(self, state):
        X = SCREEN_WIDTH - (self.ui_objects[0].get_width()*len(self.ui_objects)) - UICounter.MARGIN
        Y = SCREEN_HEIGHT - self.ui_objects[0].get_height() - UICounter.MARGIN
        self.place(X, Y)

    def place(self, x_axis, y_axis):
        last_x = x_axis
        
        for ui_object in self.ui_objects:
            ui_object.place(last_x, y_axis)
            last_x += ui_object.get_width()
            
    def set_state(self, state):
        height = state.tower.height
        ui_objs_count = len(self.ui_objects)
        
        if height < 10**ui_objs_count:
            str_height = str(height)
            while len(str_height) < ui_objs_count:
                str_height = "0" + str_height
            
            for i in range(ui_objs_count-1,-1,-1):
                str_number = str_height[i]
                self.ui_objects[i].set_image(COUNTER_PATH + str_number + IMAGE_EXTENSION)
        else:
            raise Exception("No se permite mas de " + str(ui_objs_count -1) + " pisos")

    def place_center(self, x, y, width, height):
        self._place_center_height(y, height)
        self._place_center_width(x, width)
    
    def _place_center_height(self, y, height):
        offset_rectangle = int((height-y)/2)
        offset_ui = int(self.ui_objects[0].get_height() / 2)
        for ui_object in self.ui_objects:
            ui_object.rectangle.top = y + offset_rectangle            
            ui_object.rectangle.top -= offset_ui
      
    def _place_center_width(self, x, width):
        count = len(self.ui_objects)   
        total_width = 0
        for ui_object in self.ui_objects:
            total_width += ui_object.get_width()
        
        x_pos = int(((width - x) / 2) - total_width/2)
        if x_pos < 0:
            raise Exception("Invalid centering")
        for ui_object in self.ui_objects:
            ui_object.rectangle.left = x_pos
            x_pos += ui_object.get_width()
            
    def draw(self, screen):
        for ui_object in self.ui_objects:
            screen.blit(ui_object.surface, ui_object.rectangle)

