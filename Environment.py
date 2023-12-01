import numpy as np
#import math as m
from matplotlib import pyplot as plt
from Car import CarObj
from PIL import Image

def TRACK_ROW():
    return 20

def TRACK_COL():
    return 20

def RACE_TRACK(filename):
    # Edited by Dan.
    image = Image.open(filename)
    data = np.asarray(image)
    track = np.zeros(TRACK_COL() * TRACK_ROW()).reshape(TRACK_ROW(), TRACK_COL())

    for x in range(TRACK_COL()):
        for y in range(TRACK_ROW()):
            total = sum(data[y, x])
            r, g, b = data[y, x]
            if total < 90:
                # Asphalt represented by 1
                track[y, x] = 1
            elif total > 90 and total < 350 and (r > (g + b)):
                # Gates represented by 2
                track[y, x] = 2
            elif total > 250 and total < 800:
                # Grass reprsented by 0
                track[y, x] = 0

                # Fix a few single cells that where not asphalt when all four sides were.
    for x in range(1, TRACK_COL() - 1):
        for y in range(1, TRACK_ROW() - 1):
            if track[y + 1, x] == 1 and track[y, x + 1] == 1 and track[y - 1, x] == 1 and track[y, x - 1] == 1:
                track[y, x] = 1
    return track
    #listnum = np.genfromtxt(filename, delimiter=',')
    #reshaped_listnum = listnum.reshape(TRACK_ROW(), TRACK_COL())
    #return reshaped_listnum

def track_displayer(list_data):
    #list1 = np.array([[1000, 300]])
    #list1 = np.array([[1, 2, 3], [4, 5, 6]])
    #reshaped_list1 = np.reshape(list1, (2,1))

    plt.imshow(list_data, interpolation='nearest')
    #plt.imshow(reshaped_list1, alpha=0.5)
    plt.show()
    #plt.draw()



def PIXEL_LENGTH():
    return 50




class EnvironmentClass:
    def __init__(self, track_file, start_position, orientation, racers_names):
        # Matrix for the track
        self.racers_names = racers_names# arrays of racers' names
        self.TRACK_MAT = RACE_TRACK(track_file)
        self.__carlist = []
        self.__cars_adjust(orientation)  # orient the cars'facing directions
        self.__all_cars_start_pos = start_position.copy()
        self.__load_cars()  # loads the cars into their starting positions and stores in carlist


    def NUM_OF_DRIVERS(self):
        return len(self.racers_names)

    def __load_cars(self):

        for i in range(0, self.NUM_OF_DRIVERS()):  # initialize the drivers car starting positions
            __car_obj = CarObj(self.racers_names[i], self.__all_cars_start_pos, self.orient_angle)
            self.__carlist.append(__car_obj)



    def reset_cars(self):
        for i in range(0, self.NUM_OF_DRIVERS()):
            self.__carlist[i].front_bumper_pos = self.__all_cars_start_pos
            self.__carlist[i].car_theta = self.orient_angle
            self.__carlist[i].update_Carposition()

    def __cars_adjust(self, orientation):
        orientation = orientation.upper()

        if orientation == "NORTH":
            self.orient_angle = 0

        elif orientation == "WEST":
           self.orient_angle = 90

        elif orientation == "SOUTH":
           self.orient_angle = 180

        elif orientation == "EAST":
           self.orient_angle = 270



    def car_get(self, i):
        result = self.__carlist[i]
        return result


    def reward(self, car):
        reward = 0
        x, y = car.front_bumper_history[-1][0], car.front_bumper_history[-1][1]
        if self.TRACK_MAT[int(x), int(y)] == 0:
            print("The spot was in the grass.")
            return -30

        hist_length = len(car.front_bumper_history)

        if hist_length > 1:
            present_fbumper = car.front_bumper_history[- 1]
            past_fbumper = car.front_bumper_history[-2]
            slope = (present_fbumper[1] - past_fbumper[1])/(present_fbumper[0] - past_fbumper[0])

            for x in range(int(past_fbumper[0]), int(present_fbumper[0]) + 1):
                fx = int(slope*(x-past_fbumper[0]) + past_fbumper[1])
                print("[x fx] = [", x, " ", fx," ", self.TRACK_MAT[x, fx],"]")
                if self.TRACK_MAT[x][fx] == 2:
                    reward = 100

        return reward





    #kefe dq

    def get_input_distances(self, car):
        distances = []  # Distance of the car's eight radars to the boundary
        x, y = car.front_bumper_pos
        distances.append(self.__get_distance_to_boundary(x, y))

        return distances  # A list of eight integers.

    def __get_distance_to_boundary(self, x, y):
        distances = []

        # Define directions (north, 45 degrees northeast, east, etc.)
        directions = [(0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1)]

        # Iterate through each direction
        for direction in directions:
            dx, dy = direction
            distance = 0

            # Move in the current direction until reaching the track boundary
            while self.TRACK_MAT[x, y] != 0:  # Assuming 0 represents the grass
                x += dx
                y += dy
                distance += 1

            distances.append(distance)

        return distances

    def disqualification_check(self, car):
        # Check if any tire of any car is at the track boundary (pixel value of 0 or 1)
        tires_coordinates = car.tires_history[-1]
        #print("\n", tires_coordinates)
        for tire in tires_coordinates:
            x, y = tire
            if self.TRACK_MAT[int(x)][int(y)] == 0:
                return True  # Car is off track.
        return False  # All cars are on the track.
    # Add code for crossing the finish line.








