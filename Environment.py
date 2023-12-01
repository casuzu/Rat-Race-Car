import numpy as np
#import math as m
from matplotlib import pyplot as plt
from Car import CarObj

def TRACK_ROW():
    return 1572

def TRACK_COL():
    return 2000

def RACE_TRACK(filename):
    #Edited by Dan.
    image = Image.open(filename)
    data = np.asarray(image)
    track = np.zeros(TRACK_COL()*TRACK_ROW()).reshape(TRACK_ROW(), TRACK_COL())

    for x in range(TRACK_COL()):
        for y in range(TRACK_ROW()):
            total = sum(data[y, x])
            r, g, b = data[y, x]
            if total < 90:
                #Asphalt represented by 1
                track[y, x] = 1
            elif total > 90 and total < 350 and (r>(g+b)):
                #Gates represented by 2
                track[y, x] = 2
            elif total > 250 and total < 800:
                #Grass reprsented by 0
                track[y, x] = 0  

    #Fix a few single cells that where not asphalt when all four sides were.
    for x in range(1, TRACK_COL()-1):
        for y in range(1, TRACK_ROW()-1):
            if track[y+1, x]==1 and track[y, x+1]==1 and track[y-1, x]==1 and track[y, x-1]==1:
                track[y, x] = 1
    return track    
    ##### OLD CODE #####
    #listnum = np.genfromtxt(filename, delimiter=',')
    #reshaped_listnum = listnum.reshape(TRACK_ROW(), TRACK_COL())
    #return reshaped_listnum
    ##### OLD CODE #####

def track_displayer(list_data):
    #list1 = np.array([[1000, 300]])
    #list1 = np.array([[1, 2, 3], [4, 5, 6]])
    #reshaped_list1 = np.reshape(list1, (2,1))

    plt.imshow(list_data, interpolation='nearest')
    #plt.imshow(reshaped_list1, alpha=0.5)
    plt.show()
    #plt.draw()

def NUM_OF_DRIVERS():
     return len(racers_name)

def PIXEL_LENGTH():
    return 50




class Environment:
    def __init__(self, track_file, start_position, orientation):
        # Matrix for the track
        self.TRACK_MAT = RACE_TRACK(track_file)
        self.__carlist = []
        self.__cars_adjust(orientation)  # orient the cars'facing directions
        self.__all_cars_start_pos = start_position.copy()
        self.__load_cars()  # loads the cars into their starting positions and stores in carlist


    def __load_cars(self):

        for i in range(0, NUM_OF_DRIVERS()):  # initialize the drivers car starting positions
            __car_obj = CarObj(racers_name[i], self.__all_cars_start_pos, self.orient_angle)
            self.__carlist.append(__car_obj)


    def reset_cars(self):
        for i in range(0, NUM_OF_DRIVERS()):
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


    def track(self, x, y):
        z = self.TRACK_MAT[x, y]
        return z

    def car_get(self, i):
        result = self.__carlist[i]
        return result



file_name = r"Track.csv"

#racers_name = ["Chibu", "Kefe", "Dan", "Nick", "Rupo", "Mike"]
racers_name = ["Chibu"]

#                     start_position     car_orientation
env = Environment(file_name, [1000, 300], "East")


for j in range(0, NUM_OF_DRIVERS()):
    car_item = env.car_get(j)
    print("============================")
    print(car_item.racer_name)
    print("============================")
    car_item.run()

    for step in range(0, len(car_item.tires_history)):
        print(step)
        #print(car_item.tires_history[step])
        #print(car_item.front_bumper_history[step])

    track_displayer(env.TRACK_MAT)









