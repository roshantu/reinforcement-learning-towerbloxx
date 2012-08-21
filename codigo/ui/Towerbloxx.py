#coding=utf-8

from RunInfo import RunInfo

class Towerbloxx(object):
    def __init__(self, run_info):
        self.run_info = run_info
        self.state_index = 0
    
    def get_next_state(self):
        if self.state_index < len(self.run_info.states):
            state = self.run_info.states[self.state_index]
            self.state_index += 1
            return state
        return None
        

