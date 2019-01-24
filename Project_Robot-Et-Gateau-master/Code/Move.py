import Arm_calculus as bib
import Arm as bot
import Magnet as mag
import time

class Move:

    def checkmagnets(self):
        LowerStatus = self.M0.PowerStatus
        HigherStatus = self.M5.PowerStatus
        if LowerStatus ==0 and HigherStatus==0 :
            return 0 #Both Magnets are turned off SHOULDN'T HAPPEN

        if LowerStatus ==1 and HigherStatus==0 :
            return 1 #The lower magnet is turned on

        if LowerStatus ==0 and HigherStatus==1 :
            return 2 #The higher magnet is turned on, which means the arm is in inverted mode

        if LowerStatus ==1 and HigherStatus==1 :
            return 3 #Both magnets are turned on, should only happen when using the tool.


    def __init__(self, Robot, M0, M5):
        self.M0=M0
        self.M5=M5
        self.Arm=Robot
