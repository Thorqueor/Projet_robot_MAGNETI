import pypot.dynamixel
import pypot.robot
import Arm_calculus as bib
#import bibinverse as bib
import math
import time

def radian_to_degree(angle):
    return 360.0*angle/(2*math.pi)

def degree_to_radian(angle):
    return (2*math.pi)*angle/360.0

class Arm:
    def __init__(self):
        self.bras_config = {
            'controllers': {
                'my_dxl_controller': {
                    'sync_read': False,
                    'attached_motors': ['arm'],
                    #'port': '/dev/ttyUSB0' # 'auto'
                    'port': 'auto'
                }
            },
            'motorgroups': {
                'arm': ['m0', 'm1', 'm2', 'm3', 'm4', 'm5'],
            },
            'motors': {
                'm0': {
                    'orientation': 'direct',
                    'type': 'AX-12',
                    'id': 22,
                    'angle_limit': [-102.0, 102.0],
                    #'angle_limit': [-149.0, 149.0],
                    'offset': 0.0
                },
                'm1': {
                    'orientation': 'direct',
                    'type': 'AX-12',
                    'id': 21,
                    'angle_limit': [-102.0, 102.0],
                    'offset': 0.0
                },
                'm2': {
                    'orientation': 'direct',
                    'type': 'AX-12',
                    'id': 23,
                    'angle_limit': [-102.0, 102.0],
                    'offset': 0.0
                },
                'm3': {
                    'orientation': 'direct',
                    'type': 'AX-12',
                    'id': 12,
                    'angle_limit': [-102.0, 102.0],
                    'offset': 0.0
                },
                'm4': {
                    'orientation': 'direct',
                    'type': 'AX-12',
                    'id': 11,
                    'angle_limit': [-102.0, 102.0],
                    'offset': 0.0
                },
                'm5': {
                    'orientation': 'direct',
                    'type': 'AX-12',
                    'id': 13,
                    'angle_limit': [-102.0, 102.0],
                    #'angle_limit': [-149.0, 149.0],
                    'offset': 0.0
                },
            },
        }
        self.bras = pypot.robot.from_config(self.bras_config)

        #self.first_arm_size = [0.078, 0.067, 0.067, 0.067, 0.064] OBSOLETE
        self.first_arm_size = [0.116, 0.067, 0.124, 0.067, 0.102] #SENS DIRECT

        self.first_start_position = [0,0,0]
        self.first_start_normal = [0,0,1]
        self.first_start_direction = [1,0,0]
        self.first_end_position = [0.0, 0.0, sum(self.first_arm_size)]
        self.first_end_normal = [0.0, 0.0, -1.0]
        self.first_end_direction = [1.0, 0.0, 0.0]


        self.angle_limit = [
            [degree_to_radian(-102), degree_to_radian(102)],
            [degree_to_radian(-102), degree_to_radian(102)],
            [degree_to_radian(-102), degree_to_radian(102)],
            [degree_to_radian(-102), degree_to_radian(102)],
            [degree_to_radian(-102), degree_to_radian(102)],
            [degree_to_radian(-102), degree_to_radian(102)],
        ]

        self.initialize()

    def initialize(self):
        self.start_position = self.first_start_position
        self.start_position = self.first_start_normal
        self.start_position = self.first_start_direction
        self.end_position = self.first_end_position
        self.end_normal = self.first_end_normal
        self.end_direction = self.first_end_direction
        self.arm_size = self.first_arm_size
        self.update()

    def update(self, end_position=None, end_normal=None, end_direction=None,arm_size=None):
        if end_position is None :
            end_position = self.end_position
        if end_normal is None :
            end_normal =  self.end_normal
        if end_direction is None :
            end_direction = self.end_direction
        if arm_size is None :
            arm_size = self.arm_size
        arm_calculus = bib.Arm_calculus(end_position, end_normal, end_direction, arm_size)
        if not arm_calculus.solve_min():
            print("Position, normal and direction unreachable !")
            return False
        for i in range( len(self.bras.arm) ):
            if not((arm_calculus.thetas[i] >= self.angle_limit[i][0]) and (arm_calculus.thetas[i] <= self.angle_limit[i][1])):
                print("Angle limit is reached !")
                return False
        self.end_position = bib.vec(end_position)
        self.end_normal = bib.vec(end_normal)
        self.end_direction = bib.vec(end_direction)
        self.arm_size = arm_size
        for i in range( len(self.bras.arm) ):
            self.set_angle(i, arm_calculus.thetas[i])
        return True

    def increase(self, end_position=None, end_normal=None, end_direction=None):
        if not end_position is None :
            end_position = bib.vec(self.end_position) + end_position
        if not end_normal is None :
            end_normal = bib.vec(self.end_normal) + end_normal
        if not end_direction is None :
            end_direction = bib.vec(self.end_direction) + end_direction
        return self.update(end_position=end_position, end_normal=end_normal,end_direction=end_direction)

    def __repr__(self):
        return "<p=%s, n=%s, d=%s>"%(self.end_position, self.end_normal, self.end_direction)

    def set_angle(self, i, angle):
        self.bras.arm[i].compliant = False
        self.bras.arm[i].goto_position(radian_to_degree(angle), 4)

"""
a = arm()
#time.sleep(5)
print "Moving"
########TEST DE MOUVEMENT############
time.sleep(10)
a.update([0,a.arm_size[2],0],[0,0,1],[0,1,0],a.arm_size) #MOUVEMENT EN Y
time.sleep(10)
a.update([0,0,sum(a.arm_size)],[0,0,-1],[0,1,0],a.arm_size) #REDRESSEMENT
time.sleep(10)
a.update([(a.arm_size[2]),0,0],[0,0,1],[1,0,0],a.arm_size) #MOUVEMENT INVERSE EN X ATTENTION DIRECTION
time.sleep(5)
a.update([0,0,sum(a.arm_size)],[0,0,-1],[0,1,0],a.arm_size) #REDRESSEMENT
time.sleep(5)
a.update([0,(a.arm_size[2]),0],[0,0,1],[0,-1,0],a.arm_size) #MOUVEMENT INVERSE EN -Y ATTENTION DIRECTION
time.sleep(10)
a.update([0,0,sum(a.arm_size)],[0,0,-1],[0,1,0],a.arm_size) #REDRESSEMENT
time.sleep(10)
#a.close()


a.update([a.arm_size[4],0,sum(a.arm_size)-a.arm_size[4]], [-1,0,0],[0,0,-1],a.arm_size) #MARCHE
time.sleep(5)
a.update([a.arm_size[3]+a.arm_size[4],0,a.arm_size[0]+a.arm_size[1]+a.arm_size[2]], [-1,0,0],[0,0,-1],a.arm_size) #MARCHE
time.sleep(5)



#####TEST DU REPERE DIRECT########

a.update([a.arm_size[2]+a.arm_size[3]+a.arm_size[4],0,a.arm_size[0]+a.arm_size[1]], [-1,0,0],[0,0,-1],a.arm_size) #POINTE x
time.sleep(5)
print "Moving"
a.update([0,a.arm_size[2]+a.arm_size[3]+a.arm_size[4],a.arm_size[0]+a.arm_size[1]], [0,-1,0],[0,0,-1],a.arm_size) #POINTE y
time.sleep(5)
print "Moving"



a.update([0,-(a.arm_size[2]+a.arm_size[3]+a.arm_size[4]),a.arm_size[0]+a.arm_size[1]], [0,1,0],[0,0,-1],a.arm_size) #POINTE -y MARCHE
time.sleep(5)
print "Moving"

a.update([-(a.arm_size[2]+a.arm_size[3]+a.arm_size[4]),0,a.arm_size[0]+a.arm_size[1]], [1,0,0],[0,0,-1],a.arm_size) #POINTE -x  MARCHE PAS, POINTE x
time.sleep(5)
print "Moving"

time.sleep(5)
print "Moving"
"""
