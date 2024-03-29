#coding=utf-8

from UIObject import UIObject
from UI import *
from Constants import *
import math

class UIBackground(UIObject):
    MAX_ABS_ACUM = 10000
    NEUTRAL_OFFSET = 50
    FULL_RED = 255
    FULL_GREEN = 255
    NEUTRAL = 255, 255, 255

    def __init__(self, name):
        self.acum_rewards = 0
        self.color = UIBackground.NEUTRAL
        
    def start(self, state):
        pass

    def set_state(self, state):
        self.acum_rewards += state.game.reward
        self.color = self._get_background()

    def draw(self, screen):
        screen.fill(self.color)
        
    def _get_background(self):
        in_neutral_boundaries = -UIBackground.NEUTRAL_OFFSET <= self.acum_rewards
        in_neutral_boundaries &= self.acum_rewards <= UIBackground.NEUTRAL_OFFSET
        if in_neutral_boundaries:
            return UIBackground.NEUTRAL
        else:
            percentage = self._get_percentage()
            if self.acum_rewards < 0:
                #go red
                red = UIBackground.FULL_RED
                red = min(int(math.ceil(red * percentage)), 255)
                return red,0,0
            else:
                #go green
                green = UIBackground.FULL_GREEN
                green = min(int(math.ceil(green * percentage)), 255)
                return 0,green,0
                
    def _get_percentage(self):
        mod_state = abs(self.acum_rewards)
        percentage = math.log(mod_state) / math.log(UIBackground.MAX_ABS_ACUM)
        #print "acum: " + str(self.acum_rewards) + " percentage: " + str(percentage)
        return percentage

