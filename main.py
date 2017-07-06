from arm import Arm
from detector import Detector

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