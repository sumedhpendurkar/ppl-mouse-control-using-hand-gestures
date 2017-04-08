from pymouse import PyMouse
class action:
    left_click = 1
    right_click = 2
    middle = 3
    prev_coordinates = [-1, -1]
    prev_state = ''
    def __init__(self, img_shape):
        self.mouse_cntrl = PyMouse()
        shape_y, shape_x, _ = img_shape
        print shape_x, shape_y, self.mouse_cntrl.screen_size()
        screen_x, screen_y = self.mouse_cntrl.screen_size()
        self.x_convert = screen_x * 1.0 / shape_x 
        self.y_convert = screen_y * 1.0 / shape_y
    def screen_size(self):
        return self.mouse_cntrl.screen_size()
    def zero(self):
        self.prev_state = 'zero'
        print "Unable to detect"
    def one(self, hull_p):
        print  "ek. Co-ordinates in image"+ str(hull_p)
        if self.prev_state == 'one':
            x,y = self.mouse_cntrl.position()
            self.mouse_cntrl.move(x + self.x_convert * (-1 * self.prev_coordinates[0] + hull_p[0]), 
                y + self.y_convert * (-1 * self.prev_coordinates[1] + hull_p[1]))
            self.prev_coordinates[0] = hull_p[0]
            self.prev_coordinates[1] = hull_p[1]
        else:
            self.prev_coordinates[0] = hull_p[0]
            self.prev_coordinates[1] = hull_p[1]
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
