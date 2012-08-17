

class ActionResolver(object): 
    PASS_REWARD = -1
    MISSING_REWARD = -20
    TOWER_FELL_REWARD = -100
    DOWNGRADE_STABILITY_REWARD = 30
    UPGRADE_STABILITY_REWARD = 100

    @classmethod
    def create_for(cls, environment, action):
        from PassActionResolver import PassActionResolver
        from ThrowActionResolver import ThrowActionResolver
        if action == environment.PASS:
            return PassActionResolver(environment)
        else:
            return ThrowActionResolver(environment)

    def __init__(self, environment):
        self.environment = environment

    def resolve(self):
        self.move_tower()
        self.move_crane()
        return self.environment.state, self.reward()

    def move_crane(self):
        if abs(self.environment.crane_pos) == self.environment.POSITION_BOUND:
            self.environment.crane_direction = -sign(self.environment.crane_pos)
        
        self.environment.crane_pos += self.environment.crane_direction
    

    def move_tower(self):        
        unsigned_speed_without_factor = self.environment.absolute_speed_by_position()
        unsigned_speed = math.ceil(absolute_speed_without_factor * abs(self.environment.tower_factor))
        current_speed_direction = sign(self.environment.tower_vel)

        self.environment.tower_vel = unsigned_speed * current_speed_direction

    def absolute_speed_by_position(self):
        #Idea: Imitar un pendulo... A medida que se acerca a las puntas, la velocidad disminuye y es maxima en el centro.
        vel =  (5 - abs(self.environment.tower_pos)/10) 
        return vel