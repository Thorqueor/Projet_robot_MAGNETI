import Arm_calculus as bib
import Arm as bot
import Magnet as mag
import time

class Fork(Tool):

    def pickup_fork(self, Position):
        """
        This function assumes the fork is laid up with the teeth in the direction of the robot's x axis.
        """
        orientation=checkmagnets(M0,M5)
        #TODO
        if orientation == 1:
            self.Arm.update(Position,[0,0,1],[1,0,0],self.Arm.arm_size)
            time.sleep(8)
            self.M5.Turn_ON()
            #MAYBE INSERT A SWEEP OF THE CLOSE AREA TO BETTER CATCH THE FORK

        else:
            print "SORRY, I'M NOT IN THE RIGHT ORIENTATION, I CAN'T PICK UP THE FORK T-T"


    def pickup_cake(self, Position):
        Normal = bib.normalize(bib.vec(Position))
        self.Arm.update([Position[0],Position[1],self.forklength],Normal,[0,0,-1],self.Arm.arm_size)


    def present_cake(self):
        self.Arm.update([0,0,self.Arm.arm_size-0.05],[0.5,0,0.5],[1,0,0],self.Arm.arm_size)

    def __init__(self, Robot, M0, M5):
        Tool.__init__(self, Robot, M0, M5)
        self.forklength=0.5
