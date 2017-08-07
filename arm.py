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

    def calibrated(self, x, y):
        ul = (5.9, 1.9)
        ur = (9, 1.9)

        bl = (5.8, -2.4)
        br = (8.5, -2.3)

        # interpolate x first

        x_top = (1-x) * ul[0] + x * ur[0]
        x_bot = (1-x) * bl[0] + x * br[0]

        x_interp = (1-y) * x_top + y * x_bot

        # interpolate y

        y_left = (1-y) * ul[1] + y * bl[1]
        y_right = (1-y) * ur[1] + y * br[1]

        y_interp = (1-x) * y_left + x * y_right

        return (x_interp, y_interp)

    def move_to_calibrated(self, x, y):
        # x: 0 to 1, y: 0 to 1, (0, 0) is bottom left corner, (1, 1) upper right
        # measurements from board, pivot on the left
        x_interp, y_interp = self.calibrated(x, y)
        self.move_to(x_interp, y_interp)

        """m = [[(5.9, 1.9), (7.3, 1.9), (9, 1.6)],
             [(5.9, -.5), (7.4, -.3), (8.5, -.6)],
             [(5.8, -2.4),(7.1, -2.2),(8.5, -2.3)]]

        sr = int(np.floor(y * 3))
        sc = int(np.floor(x * 3))

        tx = 0
        ty = 0

        tx = x * 2
        ty = y * 2

        if x > .5:
            tx = (x - .5) * 2
        if y > .5:
            ty = (y - .5) * 2

        x_top = m[sr][sc][0] * (1-tx) + tx * m[sr][sc+1][0]
        x_bot = m[sr+1][sc][0] * (1-tx) + tx * m[sr+1][sc+1][0]

        x_interp = (1-ty) * x_top + ty * x_bot

        y_left = m[sr+1][sc][1] * (1-ty) + ty * m[sr][sc][1]
        y_right = m[sr+1][sc+1][1] * (1-ty) + ty * m[sr][sc+1][1]

        y_interp = (1-tx) * y_left + tx * y_right

        self.move_to(x_interp, y_interp)"""


    def line(self, sx, sy, ex, ey, steps):
        self.ser.write('3 {:.2f} {:.2f} {:.2f} {:.2f} {}'.format(sx, sy, ex, ey, steps).encode('utf-8'))
        self.wait() 

    def line_calibrated(self, sx, sy, ex, ey, steps):
        sxi, syi = self.calibrated(sx, sy)
        exi, eyi = self.calibrated(ex, ey)
        self.ser.write('3 {:.2f} {:.2f} {:.2f} {:.2f} {}'.format(sxi, syi, exi, eyi, steps).encode('utf-8'))
        self.wait() 

    def draw_board(self, sx, sy, sp_size = .2):
        steps = 10

        self.move_to_calibrated(sx, sy)

        # vert
        self.line_calibrated(sx+sp_size,    sy, sx+sp_size,     sy+3*sp_size,   steps)
        self.line_calibrated(sx+2*sp_size,  sy, sx+2*sp_size,   sy+3*sp_size,   steps)

        # horiz
        self.line_calibrated(sx, sy+sp_size,    sx+3*sp_size,   sy+sp_size,     steps)
        self.line_calibrated(sx, sy+2*sp_size,  sx+3*sp_size,   sy+2*sp_size,   steps)

if __name__ == "__main__":
    arm = Arm()
    arm.connect()

    arm.led(0,1)
    arm.move_to(6.0, 0.0)
    arm.move_to(8.0, 0.0)
    arm.move_to(6.0, 0.0)

    arm.move_to(6.0, 2.0)
    arm.move_to(6.0, -2.0)
    arm.move_to(6.0, 2.0)
    arm.led(0,0)
