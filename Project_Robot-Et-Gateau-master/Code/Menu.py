import Brain

def display_menu():
    x=0
    while(x==0):
        print ("""
        Magneti control program :
        What do you want the robot to do ?
        1 : Walk to the cake box
        2 : Pick up the cake
        0 : Deactivate the Robot and quit
        """)
        selection = input()
        if(selection=="1"):
            Robot.Find_Way()
        if(selection=="2"):
            Robot.Pickup_Cake_Fork()
        if(selection=="0"):
            Robot.Deactivate()
            x=1

###Main
Robot = Brain.Brain()

display_menu()
