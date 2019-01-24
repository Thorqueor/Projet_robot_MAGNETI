import Arm_calculus as bib
import Arm as bot
import Magnet as mag
import time

class walk(Move):

    """
    Space management functions
    """


    """
    Adaptative move functions
    """


    def walkto_point(self,Position):
        """
        Position should be 3D coordinate in the form of a list [x,y,z]
        """
        orientation=Move.checkmagnets(self)
        if orientation == 1:
            self.Arm.update([Position[0],Position[1],0.03],[0,0,1],[0,1,0],self.Arm.arm_size)
            time.sleep(8)
            self.Arm.update(Position,[0,0,1],[0,1,0],self.Arm.arm_size)

            self.M5.Turn_ON()
            time.sleep(3)
            self.M0.Turn_OFF()


        if orientation == 2: #NOT FINISHED, NEED TO FIX THE DIRECTION TODO
            Direction = bib.normalize(bib.vec(Position))
            for i in range(len(Direction)):
                Direction[i]=Direction[i]*(-1.0)            #Arm.update(Position,[0,0,1],[0,1,0],Arm.arm_size)
            self.Arm.update([Position[0],Position[1], 0.03],[0,0,1],Direction,self.Arm.arm_size) #NEED TO TEST
            time.sleep(8)
            self.Arm.update(Position,[0,0,1],Direction,self.Arm.arm_size) #NEED TO TEST
            time.sleep(8)
            self.M0.Turn_ON()
            time.sleep(3)
            self.M5.Turn_OFF()
            time.sleep(3)
        self.reset_motors()

    def reset_motors(self):
        self.Arm.update([0,0,sum(self.Arm.arm_size)],[0,0,-1],[0,1,0],self.Arm.arm_size) #ARM PUTS ITSELF UPRIGHT
        time.sleep(8)


    """
    Hardcoded Move functions
    """
    def move_x(self):
        Arm.update([self.max_distance,0,0],[0,0,1],[0,1,0],Arm.arm_size) #MOUVEMENT EN X
        time.sleep(8)
        M5.Turn_ON()
        M0.Turn_OFF()
        self.reset_motors()

    def move_y(self):
        Arm.update([0,self.max_distance,0],[0,0,1],[0,1,0],Arm.arm_size) #MOUVEMENT EN Y
        time.sleep(8)
        M5.Turn_ON()
        M0.Turn_OFF()
        self.reset_motors()

    def move_minus_y(self):
        Arm.update([0,-self.max_distance,0],[0,0,1],[0,1,0],Arm.arm_size) #MOUVEMENT EN Y
        time.sleep(8)
        M5.Turn_ON()
        M0.Turn_OFF()
        self.reset_motors()

    def inv_move_x(self):
        Arm.update([(self.max_distance),0,0],[0,0,1],[1,0,0],Arm.arm_size) #MOUVEMENT INVERSE EN X ATTENTION DIRECTION
        time.sleep(8)
        M0.Turn_ON()
        M5.Turn_OFF()
        self.reset_motors()

    def inv_move_y(self):
        Arm.update([0,(self.max_distance),0],[0,0,1],[0,-1,0],Arm.arm_size) #MOUVEMENT INVERSE EN -Y ATTENTION DIRECTION
        time.sleep(10)
        M0.Turn_ON()
        M5.Turn_OFF()
        self.reset_motors()

    def __init__(self, Robot, M0, M5):
        Move.__init__(self, Robot, M0, M5)
        self.max_distance = Robot.arm_size[2]


####MAIN
#A = bot.arm()
#M0 = mag.Magnet(12,25)
#M5 = mag.Magnet(33,25)
