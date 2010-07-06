import lib

class code(object):
    def __init__(self,robot,init = None):
        self.ro = robot
        
        if init == None:
            self.cmds = []
        else:
            self.cmds=init
        self.cur_cmd = 0
        
    def run_cmd(self):

        if len(self.cmds) > 0: 
            #check for end of program blocks first...
            if self.cmds[self.cur_cmd] == 'end':
                return
            if self.cmds[self.cur_cmd] == 'tl':
                self.ro.turn('left')
            elif self.cmds[self.cur_cmd] == 'tr':
                self.ro.turn('right')
            elif self.cmds[self.cur_cmd] == 'move_fwd':
                self.ro.move_fwd()
            elif self.cmds[self.cur_cmd] == 'move_bck':
                self.ro.move_bck()
            elif self.cmds[self.cur_cmd] == 'pick_up':
                self.ro.pick_up()
            elif self.cmds[self.cur_cmd] == 'put_down':
                self.ro.put_down()
            
            if self.cur_cmd + 1  == len(self.cmds):
                self.cur_cmd = 0
            else:
                self.cur_cmd += 1
                
class interface(object):
    def __init__(self,robot):
        self.ro = robot
    
    @lib.decorators.disabled
    def draw(self, screen):
        screen.blit(self.surf, self.rect)