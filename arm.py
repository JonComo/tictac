import serial
from time import sleep
import numpy as np

class Arm():
    def __init__(self):
        pass

    def connect(self):
        loc = "/dev/cu.usbmodem1421"
        self.ser = serial.Serial(loc, 115200)
        if self.ser is None:
            print("error, no serial")
            print("Don't forget to change the serial location for your system. Currently set to: {}".format(loc))
        
        self.wait() # wait until ready
        sleep(1)

    def wait(self):
        while True:
            if self.ser.readline():
                return

    def led(self, color, on):
        self.ser.write('4 {} {}'.format(color, on).encode('utf-8'))
        self.wait()

    def pen_up(self):
        self.ser.write(b'0')
        self.wait()

    def pen_down(self):
        self.ser.write(b'1')
        self.wait()

    def move_to(self, x, y):
        self.ser.write('2 {:.2f} {:.2f}'.format(x, y).encode('utf-8'))
        self.wait()

    def line(self, sx, sy, ex, ey, steps):
        self.ser.write('3 {:.2f} {:.2f} {:.2f} {:.2f} {}'.format(sx, sy, ex, ey, steps).encode('utf-8'))
        self.wait() 

    def draw_board(self, sx, sy):
        sp_size = 2 # space size inches
        steps = 5

        self.move_to(sx, sy)

        # vert
        self.line(sx+sp_size,    sy, sx+sp_size,     sy+3*sp_size,   steps)
        self.line(sx+2*sp_size,  sy, sx+2*sp_size,   sy+3*sp_size,   steps)

        # horiz
        self.line(sx, sy+sp_size,    sx+3*sp_size,   sy+sp_size,     steps)
        self.line(sx, sy+2*sp_size,  sx+3*sp_size,   sy+2*sp_size,   steps)

if __name__ == "__main__":
    arm = Arm()
    arm.connect()

    arm.led(0,1)
    arm.move_to(15.0, 0.0)
    arm.move_to(10.0, 0.0)
    arm.move_to(15.0, 0.0)
    arm.led(0,0)

    arm.led(2,1)
    arm.line(15.0, 0.0, 10.0, 0.0, 10)
    arm.line(10.0, 0.0, 10.0, 5.0, 10)
    arm.line(10.0, 0.0, 10.0, -5.0, 10)

    arm.move_to(15.0, 0.0)

    arm.led(2,0)
