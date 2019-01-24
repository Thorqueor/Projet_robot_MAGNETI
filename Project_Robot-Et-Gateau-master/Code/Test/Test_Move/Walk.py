import bib
import bot
import Magnet as mag
import time

"""
Space management functions
"""
def checkmagnets(M0,M5):
    LowerStatus = M0.PowerStatus
    HigherStatus = M5.PowerStatus
    if LowerStatus ==0 and HigherStatus==0 :
        return 0 #Both Magnets are turned off SHOULDN'T HAPPEN
    if LowerStatus ==1 and HigherStatus==0 :
        return 1 #The lower magnet is turned on
    if LowerStatus ==0 and HigherStatus==1 :
        return 2 #The higher magnet is turned on, which means the arm is in inverted mode
    if LowerStatus ==1 and HigherStatus==1 :
        return 3 #Both magnets are turned on, should only happen when using the tool.


"""
Adaptative move functions
"""

def checkmagnets(M0,M5):
    LowerStatus = M0.PowerStatus
    HigherStatus = M5.PowerStatus
    if LowerStatus ==0 and HigherStatus==0 :
        return 0 #Both Magnets are turned off SHOULDN'T HAPPEN
    if LowerStatus ==1 and HigherStatus==0 :
        return 1 #The lower magnet is turned on

    if LowerStatus ==0 and HigherStatus==1 :
        return 2 #The higher magnet is turned on, which means the arm is in inverted mode

    if LowerStatus ==1 and HigherStatus==1 :
        return 3 #Both magnets are turned on, should only happen when using the tool.


def walkto_point(Robot,M0,M5,Position):
    """
    Position should be 3D coordinate in the form of a list [x,y,z]
    """
    orientation=checkmagnets(M0,M5)
    if orientation == 1:
        Robot.update(Position,[0,0,1],[0,1,0],Robot.arm_size)
        time.sleep(8)
        M5.Turn_ON()
        M0.Turn_OFF()


    if orientation == 2: #NOT FINISHED, NEED TO FIX THE DIRECTION TODO
        Direction = bib.normalize(bib.vec(Position))
        #Robot.update(Position,[0,0,1],[0,1,0],Robot.arm_size)
        Robot.update(Position,[0,0,1],Direction,Robot.arm_size) #NEED TO TEST
        time.sleep(8)
        M5.Turn_ON()
        M0.Turn_OFF()
        Robot.update([0,0,sum(Robot.arm_size)],[0,0,-1],[0,1,0],Robot.arm_size) #ARM PUTS ITSELF UPRIGHT
        time.sleep(8)

    """
    Hardcoded Move functions
    """
def move_x(Robot,M0,M5):
    Robot.update([Robot.arm_size[2],0,0],[0,0,1],[0,1,0],Robot.arm_size) #MOUVEMENT EN X
    time.sleep(8)
    M5.Turn_ON()
    M0.Turn_OFF()
    Robot.update([0,0,sum(Robot.arm_size)],[0,0,-1],[0,1,0],Robot.arm_size) #REDRESSEMENT
    time.sleep(8)

def move_y(Robot,M0,M5):
    Robot.update([0,Robot.arm_size[2],0],[0,0,1],[0,1,0],Robot.arm_size) #MOUVEMENT EN Y
    time.sleep(8)
    M5.Turn_ON()
    M0.Turn_OFF()
    Robot.update([0,0,sum(Robot.arm_size)],[0,0,-1],[0,1,0],Robot.arm_size) #REDRESSEMENT
    time.sleep(8)

def move_minus_y(Robot,M0,M5):
    Robot.update([0,-Robot.arm_size[2],0],[0,0,1],[0,1,0],Robot.arm_size) #MOUVEMENT EN Y
    time.sleep(8)
    M5.Turn_ON()
    M0.Turn_OFF()
    Robot.update([0,0,sum(Robot.arm_size)],[0,0,-1],[0,1,0],Robot.arm_size) #REDRESSEMENT
    time.sleep(8)

def inv_move_x(Robot,M0,M5):
    Robot.update([(Robot.arm_size[2]),0,0],[0,0,1],[1,0,0],Robot.arm_size) #MOUVEMENT INVERSE EN X ATTENTION DIRECTION
    time.sleep(8)
    M0.Turn_ON()
    M5.Turn_OFF()
    Robot.update([0,0,sum(Robot.arm_size)],[0,0,-1],[0,1,0],Robot.arm_size) #REDRESSEMENT
    time.sleep(8)

def inv_move_y(Robot,M0,M5):
    Robot.update([0,(Robot.arm_size[2]),0],[0,0,1],[0,-1,0],Robot.arm_size) #MOUVEMENT INVERSE EN -Y ATTENTION DIRECTION
    time.sleep(10)
    M0.Turn_ON()
    M5.Turn_OFF()
    Robot.update([0,0,sum(Robot.arm_size)],[0,0,-1],[0,1,0],Robot.arm_size) #REDRESSEMENT
    time.sleep(10)


####MAIN

A = bot.arm()
M0 = mag.Magnet(12,25)
M5 = mag.Magnet(33,25)
M0.Turn_ON()
time.sleep(2)
move_y(A, M0, M5)
inv_move_y(A, M0, M5)
M0.destroy()
M5.destroy()
