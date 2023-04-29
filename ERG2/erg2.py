import numpy as np
import matplotlib.pyplot as plt
import csv
#from enum import Enum

def safe_csv_read(csvstring):            #from python docs: https://docs.python.org/3/library/csv.html#examples
    output=[]
    with open(csvstring, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output.append(row)
    return output

#class Column(Enum):
#    ArtGaleries = 0 
#    DanceClubs = 1
#    JuiceBars = 2
#    Restaurants = 3
#    Museums = 4
#    Resorts = 5
#    Parks = 6
#    Beaches = 7
#    Theaters = 8 
#    ReligiousInstitutions = 9

def manhatan_distance(point1_x,point1_y,point2_x,point2_y):   # eucledian distance is harder to compute
    return np.abs(point1_x-point2_x) + np.abs(point1_y-point2_y)

def find_closest_point(arr,point):
    output=[]
    for i in arr:
        output.append(manhatan_distance(i[0],point[0],i[1],point[1]))
    return np.argmin(output)


# def make_colors(pairs):
    
def make_groups(data,points):
    output=[]
    for i in data:
        tmp=[]
        for j in points:
            tmp.append(data[point])
    return output

data=safe_csv_read('source.csv')
data.pop(0)
#for i in data:  # After examining the data set, the user id is linearly assigned. So we don't need it as it can be recreated by adding 1 to the current index
#    i.pop(0)
                # At this point, the dataset is just a grid of numbers with each row being a user.

#print(data[0][0])
x=[]
y=[]
for i in data:
    x.append(i[4])
    y.append(i[12])
plt.scatter(x,y)


x=[]
y=[]
for i in data:
    x.append(i[4])
    y.append(i[12])
plt.scatter(x,y)

# plt.scatter(y)
plt.show()