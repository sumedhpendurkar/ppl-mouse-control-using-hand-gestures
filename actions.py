from pymouse import PyMouse
class action:
    left_click = 1
    right_click = 2
    middle = 3
    prev_state = ''
    screen_x = 0
    screen_y = 0
    def __init__(self):
        self.mouse_cntrl = PyMouse()
        self.screen_x, self.screen_y = self.mouse_cntrl.screen_size()
    def screen_size(self):
        return self.mouse_cntrl.screen_size()
    def one(self, hull_p):
        print "ek"+str(hull_p)
        self.mouse_cntrl.move(2 * hull_p[0],2 * hull_p[1])
        self.prev_state = 'one'
    def two(self):
        print "don"
        if self.prev_state == 'two':
            return
        current_x, current_y = self.mouse_cntrl.position()
        self.mouse_cntrl.click(current_x,current_y, self.left_click)
        self.prev_state = 'two'
    def three(self):
        print "tiin"
        if self.prev_state == 'three':
            return
        current_x, current_y = self.mouse_cntrl.position()
        self.mouse_cntrl.click(current_x, current_y, self.right_click)
        self.prev_state = 'three'
    def four(self):
        print "char"
    def done(self, a):
        pass
    def dtwo(self):
        pass
    def dthree(self):
        pass
    def dfour(self):
        pass
