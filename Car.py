
#def __func() denotes private function anything else is public. Same for variables.
# e.g. __x is private
import numpy as np
import math as m

def WIDTH():
    carWidth = 30
    return carWidth

def LENGTH():
    carLength = 50
    return carLength

def RADIANS(deg):
    deg = deg % 360  # normalize car value in degrees.
    theta = deg * m.pi/ 180.0
    return theta

def THETA_INCREMENT(): # the value by the car turn if it is to turn. 20 is preferred.
    return 20.0
def MAX_SPEED():
    return 200 # 50 is standard max car speed.

def TIME(): # the time it takes to reach the full car speed.
    return 20

# Ideally a precise set of driving instruction per frame.
actions_1 =np.array([
                            ["Straight", "Accelerate"], ["Straight", "Accelerate"],
                            ["Straight", "Accelerate"], ["Straight", "Accelerate"],
                            ["Right", "Brake"], ["Right", "Brake"],
                            ["Straight", "Accelerate"],["Straight", "Coast"],
                            ["Straight", "Brake"],["Right", "Brake"],
                            ["Right", "Brake"], ["Straight", "Accelerate"]
                             ])
class CarObj:

    # tire positions on car
    # t[0]----t[1]
    # |         |
    # |  Car    |
    # |  Shape  |
    # |         |
    # t[2]----t[3]

    __center = np.zeros(2).reshape(1, 2) # center of the car [x, y] position size: [1x2].
    __tires = np.zeros(8).reshape(4, 2) # list of tires [x, y] positions size: [4x1x2].
    front_bumper_pos = [] # front bumper [x, y] size: [1x2].
    __car_start_pos = None #initial [x, y] starting position of the car.
    tires_history = []
    front_bumper_history = []

    def __init__(self, racer_name, front_bumper_pos, theta):  # Constructor
        self.racer_name = racer_name # driver's name
        self.front_bumper_pos = front_bumper_pos.copy()
        self.car_theta = theta  # car theta is the angle of turn.
        self.__speed = 0   # speed of the car.
        self.__accelerate = 30 # car's acceleratino rate.
        self.__jerk = 1 # car's jerk rate. jerk is the rate of change of the acceleration.
        self.__decelerate = 0 # car's deceleration rate.
        self.__djerk = 0.01 # car's deceleration rate
        self.update_Carposition() # update the car's center and tires.

        # returns the start position of the front tires at the start of the race.
        self.__car_start_pos = self.front_bumper_pos.copy()

    def update_car_history(self):
        self.front_bumper_history.append(self.front_bumper_pos.copy())
        self.tires_history.append([self.__tires[0].copy(), self.__tires[1].copy(),
                                       self.__tires[2].copy(), self.__tires[3].copy()])

    def update_Carposition(self): # calculate and update the car's center and tires.
        #[0][0][Ft1]----------[0][1][Ft2]
        #|                              |
        #|                              |
        #|                              |
        #|                              |
        #[1][0][Bt3]----------[1][1][Bt4]

        fx, fy = self.front_bumper_pos[0], self.front_bumper_pos[1] # position of the front bumper.

        #obtaining the XY coordinates of the tires using the front bumper XY position.
        tire1_x = fx - 0.5 * WIDTH() * m.cos(RADIANS(self.car_theta)) # tire1x
        tire1_y = fy + 0.5 * WIDTH() * m.sin(RADIANS(self.car_theta)) # tire1y

        tire2_x = fx + 0.5 * WIDTH() * m.cos(RADIANS(self.car_theta))  # tire2x
        tire2_y = fy - 0.5 * WIDTH() * m.sin(RADIANS(self.car_theta))  # tire2y

        tire4_x = tire2_x - LENGTH() * m.cos(RADIANS(self.car_theta + 90))  # tire4x
        tire4_y = tire2_y - LENGTH() * m.sin(RADIANS(-(self.car_theta + 90)))  # tire4y

        tire3_x = tire4_x + WIDTH() * m.cos(RADIANS(self.car_theta + 180))  # tire3x
        tire3_y = tire4_y - WIDTH() * m.sin(RADIANS(self.car_theta + 180))  # tire3y

        centerX = fx + 0.5 * LENGTH() * m.cos(RADIANS(self.car_theta - 90)) # car_center xpos
        centerY = fy + 0.5 * LENGTH() * m.sin(RADIANS(self.car_theta + 90)) # car_center ypos


        self.__center = [centerX, centerY]

        # Updating the tire list
        self.__tires[0] = [tire1_x, tire1_y] #tire1
        self.__tires[1] = [tire2_x, tire2_y] #tire2
        self.__tires[2] = [tire3_x, tire3_y] #tire3
        self.__tires[3] = [tire4_x, tire4_y] #tire4

        self.update_car_history()

    def __calcCar_motion(self, turn): # calculate and update the car's turn and orientation
        if self.__speed <= 0: # If car has been decelerated below zero to a negative value.
            self.__speed = 0

        # car_theta + 90 to face the car upright
        # Calculate the car's new position after turn car_theta + 90

        self.front_bumper_pos[0] = self.__car_start_pos[0] + (self.__speed * m.cos(RADIANS(self.car_theta + 90)))
        self.front_bumper_pos[1] = self.__car_start_pos[1] - (self.__speed * m.sin(RADIANS(self.car_theta + 90)))

        # if no car turn was choosen, don't increase car turn angle

        if turn == 0:
            theta_increment = 0.0
        else:
            theta_increment = THETA_INCREMENT()


        if turn == -1: # turn left
            self.car_theta = self.car_theta + theta_increment

        elif turn == 1: # turn right
            self.car_theta = self.car_theta - theta_increment

        #Set the new position that the car moved to as the car starting position for the new draw.
        self.__car_start_pos[0] = self.front_bumper_pos[0]
        self.__car_start_pos[1] = self.front_bumper_pos[1]


    def __calc_speed(self, accel_or_brake): # Calculates by how much the car should accelerate or move.
        if accel_or_brake == 1: #if accelerate is picked
            if self.__speed < MAX_SPEED(): # if max speed is not yet reached
                #increase car's accleration and speed and reset decelerate to its default value.
                self.__decelerate = self.__djerk
                self.__accelerate += self.__jerk
                self.__speed = self.__speed + self.__accelerate * (TIME()/ 20)



        elif accel_or_brake == -1: # if brake is picked.
            # if car speed is still above the value 0
            if self.__speed > 0:
                self.__speed = self.__speed - self.__decelerate * (TIME()/ 20)
                self.__decelerate += self.__djerk # if brake is pressed multiple times.


        elif accel_or_brake == 0: # if maintain the same velocity or speed is chosen -> coast.
            self.__decelerate = self.__djerk
            self.__speed = self.__speed + self.__accelerate * (TIME()/ 20) # coast

        # if the current car speed goes over the max car speed
        if self.__speed > MAX_SPEED():
            self.__speed = MAX_SPEED()




    def __interprete_NN_decision(self, do_these): # Interpret Neural network decisions.
                                        # Actions array elements are set to mimic possible Neural
                                        # network decisions. NN stands for Neural Network.

        left, straight, right = "Left", "Straight", "Right"
        accelerate, coast, brake = "Accelerate", "Coast", "Brake" # coast is equal to keeping the same
                                                                  # velocity. or not accelerating.

        turn = 0 # -1, 0, 1 means car is to turn left, stay straight or turn right respectively.

        if do_these[0] == left:
            turn = -1

        elif do_these[0] == straight:
            turn = 0

        elif do_these[0] == right:
            turn = 1


        if do_these[1] == accelerate:
            self.__calc_speed(1)

        elif do_these[1] == coast:
            self.__calc_speed(0)

        elif do_these[1] == brake:
            self.__calc_speed(-1)
            if self.__speed == 0: # if car speed is 0. Stop turning and set the car straight.
                turn = 0


        # Move the car.
        self.__calcCar_motion(turn)
        self.update_Carposition()

    def displayCar_Info(self): #Displays all the car's public attributes.
        #print(F'Car name = {self.racer}')

        print(F'Car_theta = {self.car_theta}')
        print(F'Car FBumper ={self.front_bumper_pos}')

        #print(F'Car center = {self.__center}')

        print(F'Car Accelerate = {self.__accelerate}')
        print(F'Car Speed = {self.__speed}')




    def run(self):

        for i, element in enumerate(actions_1):
            print("\n", i, " ",actions_1[i])
            self.__interprete_NN_decision(element)
            self.displayCar_Info()


    #def NN_interim(self, radar_info):
     #   if (m.absradar_info[1])== :