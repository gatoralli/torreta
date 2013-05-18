import os
import pyglet
from pyfirmata import Arduino, util
import math


class Window(pyglet.window.Window):

    def __init__(self):
        super(Window, self).__init__()
        self.board = None
        self.resetValues()
        
    def set_exclusive_mouse(self, exclusive):
        super(Window, self).set_exclusive_mouse(exclusive)
        self.exclusive = exclusive
    
    def on_mouse_press(self, x, y, button, modifiers):
        window.led.write(1)
        
    def on_mouse_release(self, x, y, button, modifiers):
        window.led.write(0)
            
    def on_mouse_motion(self, x, y, dx, dy):
        if self.board:
            self.dirValue = int(dx >= 0)
            
            f = clamp(abs(dx / 100.0), 0, 1)
            self.pwmValue = math.pow(f, 0.5) * 0.5 + 0.5
            
    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x, y, dx, dy)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            pyglet.app.exit()
            
    def update(self, dt):
        self.dir.write(self.dirValue)
        self.board.pass_time(0.015)
        self.pwm.write(self.pwmValue)
        self.board.pass_time(0.015)
        self.resetValues()
        
    def resetValues(self):
        self.dirValue = 0
        self.pwmValue = 0.0


def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def getBoard(port):
    print "Connecting to %s..." % port
    board = Arduino(port)
    print "Connected"
    return board

if __name__ == "__main__":
    window = Window()
    window.set_exclusive_mouse(True)

    grep = "ls /dev | grep -iE 'ttyusb|ttyacm'"
    ports = os.popen(grep).read().split("\n")

    if len(ports) > 1:
        port = "/dev/" + ports[0]
        board = getBoard(port)
        
        window.board = board
        window.pwm = board.get_pin('d:3:p')
        window.dir = board.get_pin('d:12:o')
        window.led = board.get_pin('d:13:o')
        
        pyglet.clock.schedule_interval(window.update, 0.05)
        pyglet.app.run()
    else:
        print "No board connected."
