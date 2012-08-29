#coding=utf-8
from random import random

from environment import Environment

class Agent(object):
    def __init__(self, environment):
        self.environment = environment
        
    def q_value(self, key):
        print self.q_matrix.get(key, 0)
        return self.q_matrix.get(key, 0)

    def e_value(self,key):
        return self.elegibilities.get(key,0)
    
    def learn(self):
        for i in range(1000):
            self.run_episode()
            print "Episodio numero: " + str(i) #TODO: Elminar
            
    def choose_action(self, state):
        throw_val = self.q_value((state, Environment.THROW))
        pass_val = self.q_value((state, Environment.PASS))
        if throw_val >= pass_val:
            action = Environment.THROW
            opposite_action = Environment.PASS
        else:
            action = Environment.PASS
            opposite_action = Environment.THROW
        
        return action if random() > self.epsilon else opposite_action

    def what_did_i_learned(self):
        print "#of States: " + str(len(self.q_matrix.keys()))
