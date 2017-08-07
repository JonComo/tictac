from arm import Arm
from time import sleep
from cam import Cam

from detector import Detector

AI = "T3_AI"
SYSTEM = "SYSTM"

def say(name, message):
    print("{}: {}".format(name, message))

def wait_for_user():
    arm.led(0,1)
    input("press Enter to continue")
    arm.led(0,0)

def sense_board():
    say(AI, "let me see....")
    arm.led(2,1)
    imgs = cam.get_k(20)
    arm.led(2,0)
    return imgs

if __name__ == "__main__":
    img_rows, img_cols = 64, 64

    # setup arm
    say(SYSTEM, "initializing arm...")
    arm = Arm()
    arm.connect()
    say(SYSTEM, "OK")

    # setup camera
    say(SYSTEM, "initializing camera...")
    cam = Cam(img_rows, img_cols)
    say(SYSTEM, "OK")

    # setup brain
    say(SYSTEM, "initializing neural network...")
    d = Detector(64, 64)
    say(SYSTEM, "OK")

    # lift up the pen
    arm.pen_up()

    say(AI, "Wanna play?")
    wait_for_user()

    # start a new game
    say(SYSTEM, "starting new game")
    #say(AI, "drawing the board for you...")
    #arm.draw_board(.1, .2, sp_size=.25)

    # wait
    arm.move_to_calibrated(-.1, 0.5)
    
    say(AI, "make your move...")
    wait_for_user()
    
    # sense the board
    imgs = sense_board()

    prediction = d.predict_average(imgs)
    say(AI, "I predict a board state of: {}".format(prediction))

    say(AI, "wait!! don't kill me!!!")
    wait_for_user()

    # make move based on board state
    
    # repeat until game draw or game over