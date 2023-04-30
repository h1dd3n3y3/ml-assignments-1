import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from sklearn.cluster import KMeans
#from datetime import datetime
#day_of_year = datetime.strptime(date_string, format).timetuple().tm_yday 
#from enum import Enum

class dataset_attributes:
    Travel_Duration=4
    Traveler_Age=6
    Accomodation_Cost=10
    Transportation_Cost=12

def safe_csv_read(csvstring):            #from python docs: https://docs.python.org/3/library/csv.html#examples
    output=[]
    with open(csvstring, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output.append(row)
    return output

#def manhatan_distance(point1_x,point1_y,point2_x,point2_y):   # eucledian distance is harder to compute
    #return np.abs(point1_x-point2_x) + np.abs(point1_y-point2_y)

def eucledian_distance(point1,point2):
    return np.sqrt(np.sum(np.square(point1 - point2)))

def split_data(data,cluster_centers,labels):
    output=[]
    for j in range(0, cluster_centers.shape[0]):
        output.append([])
    k=0
    #for i in range(0,data.shape[0]):
        #output[j].append(data[i])
    for i in data:
        output[labels[k]].append(i)
        k=k+1
    return output

def get_cluster_radii(cluster_centers,labels,subset):
    output=np.zeros(cluster_centers.shape[0])
    distances=np.zeros((cluster_centers.shape[0],subset.shape[0]))
    spdat=split_data(subset, cluster_centers, labels)
    spdatlen=[]
    #print("i ran")
    #print(spdat)
    #print(spdat[0][0])
    for k in range(0,cluster_centers.shape[0]):
        j=0
        for i in spdat[k]:
            j=j+1
        spdatlen.append(j)
    for i in range (0,cluster_centers.shape[0]):
        for j in range(0,spdatlen[i]):
            distances[i][j]=eucledian_distance(spdat[i][j],  cluster_centers[i])
    for i in labels:
        output[i]=np.amax(distances[i])
    return output
#######################################################################################################
data=safe_csv_read('source.csv')
data.pop(0)
cmap = { 0:'b',1:'y',2:'k',3:'g',4:'r' }
fig, axis=plt.subplots(2, 3)
#######################################################################################################  1
x=[]
y=[]
for i in data:
    #x.append(pd.to_numeric(i[dataset_attributes().Accomodation_Cost])+pd.to_numeric(i[dataset_attributes().Transportation_Cost]))
    x.append(pd.to_numeric(i[dataset_attributes().Traveler_Age]))
    y.append(pd.to_numeric(i[dataset_attributes().Travel_Duration]))
#plt.scatter(x,y)
subset=np.array(list(zip(x,y)))
#print(subset)

kmeans= KMeans(n_clusters=2, init='random', n_init='auto' , algorithm='lloyd').fit(subset) # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
radii=get_cluster_radii(kmeans.cluster_centers_, kmeans.labels_, subset)

#print(kmeans.cluster_centers_)
#print(kmeans.labels_)
#print(radii)
#print(data)

j=0
for i in kmeans.cluster_centers_:
    circle=plt.Circle(i, radii[j], color=cmap[j], fill=False)
    axis[0][0].add_patch(circle)
    j=j+1

axis[0][0].scatter(x,y, c=kmeans.labels_)
print()
print("Traveler Age/Travel Duration")
print("The centroids of the 2 clusters are:")
print("{} {}".format(kmeans.cluster_centers_[0], kmeans.cluster_centers_[1]))
print("The radii are:")
print("{} {}".format(radii[0], radii[1]))
subsets=split_data(data, kmeans.cluster_centers_, kmeans.labels_)
#print(subsets[0])
total=0
for i in data:
    total=total+1
cluster1=0
for i in subsets[0]:
    cluster1=cluster1+1 # need to make a pink floyd refference here
cluster2=0
for i in subsets[1]:
    cluster2=cluster2+1
print("And the clusters have {} and {} data points out of the {} total points respectively".format(cluster1, cluster2, total))
print()
print("----------------------------------------------------------------------------------------")
#######################################################################################################  2


x=[]
y=[]
for i in subsets[0]:
    #x.append(pd.to_numeric(i[dataset_attributes().Accomodation_Cost])+pd.to_numeric(i[dataset_attributes().Transportation_Cost]))
    x.append(pd.to_numeric(i[dataset_attributes().Accomodation_Cost]))
    #print(i[dataset_attributes().Accomodation_Cost])
    y.append(pd.to_numeric(i[dataset_attributes().Travel_Duration]))
#plt.scatter(x,y)
subset=np.array(list(zip(x,y)))

#print(subset)

kmeans= KMeans(n_clusters=2, init='random', n_init='auto' , algorithm='lloyd').fit(subset) # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
radii=get_cluster_radii(kmeans.cluster_centers_, kmeans.labels_, subset)

#print(kmeans.cluster_centers_)
#print(kmeans.labels_)
#print(radii)
#print(data)

j=0
for i in kmeans.cluster_centers_:
    circle=plt.Circle(i, radii[j], color=cmap[j], fill=False)
    axis[0][1].add_patch(circle)
    j=j+1

axis[0][1].scatter(x,y, c=kmeans.labels_)

print()
print("From cluster 1:")
print()
print("Accomodation Cost/Travel Duration")
print("The centroids of the 2 clusters are:")
print("{} {}".format(kmeans.cluster_centers_[0], kmeans.cluster_centers_[1]))
print("The radii are:")
print("{} {}".format(radii[0], radii[1]))
subsetss=split_data(subsets[0], kmeans.cluster_centers_, kmeans.labels_)
#print(subsets[0])
total=0
for i in subsets[0]:
    total=total+1
cluster1=0
for i in subsetss[0]:
    cluster1=cluster1+1
cluster2=0
for i in subsetss[1]:
    cluster2=cluster2+1
print("And the clusters have {} and {} data points out of the {} total points respectively".format(cluster1, cluster2, total))
print()
print("----------------------------------------------------------------------------------------")
#######################################################################################################  3
x=[]
y=[]
for i in subsets[0]:
    x.append(pd.to_numeric(i[dataset_attributes().Transportation_Cost]))
    y.append(pd.to_numeric(i[dataset_attributes().Travel_Duration]))
subset=np.array(list(zip(x,y)))

kmeans= KMeans(n_clusters=2, init='random', n_init='auto' , algorithm='lloyd').fit(subset) # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
radii=get_cluster_radii(kmeans.cluster_centers_, kmeans.labels_, subset)

#print(kmeans.cluster_centers_)
#print(kmeans.labels_)
#print(radii)
#print(data)

j=0
for i in kmeans.cluster_centers_:
    circle=plt.Circle(i, radii[j], color=cmap[j], fill=False)
    axis[0][2].add_patch(circle)
    j=j+1

axis[0][2].scatter(x,y, c=kmeans.labels_)

print()
print("From cluster 1:")
print()
print("Transportation Cost/Travel Duration")
print("The centroids of the 2 clusters are:")
print("{} {}".format(kmeans.cluster_centers_[0], kmeans.cluster_centers_[1]))
print("The radii are:")
print("{} {}".format(radii[0], radii[1]))
subsetss=split_data(subsets[0], kmeans.cluster_centers_, kmeans.labels_)
#print(subsets[0])
total=0
for i in subsets[0]:
    total=total+1
cluster1=0
for i in subsetss[0]:
    cluster1=cluster1+1
cluster2=0
for i in subsetss[1]:
    cluster2=cluster2+1
print("And the clusters have {} and {} data points out of the {} total points respectively".format(cluster1, cluster2, total))
print()
print("----------------------------------------------------------------------------------------")
#######################################################################################################  4
x=[]
y=[]
for i in subsets[1]:
    #x.append(pd.to_numeric(i[dataset_attributes().Accomodation_Cost])+pd.to_numeric(i[dataset_attributes().Transportation_Cost]))
    y.append(pd.to_numeric(i[dataset_attributes().Traveler_Age]))
    x.append(pd.to_numeric(i[dataset_attributes().Accomodation_Cost]))
#plt.scatter(x,y)
subset=np.array(list(zip(x,y)))
#print(subset)

kmeans= KMeans(n_clusters=2, init='random', n_init='auto' , algorithm='lloyd').fit(subset) # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
radii=get_cluster_radii(kmeans.cluster_centers_, kmeans.labels_, subset)

#print(kmeans.cluster_centers_)
#print(kmeans.labels_)
#print(radii)
#print(data)

j=0
for i in kmeans.cluster_centers_:
    circle=plt.Circle(i, radii[j], color=cmap[j], fill=False)
    axis[1][0].add_patch(circle)
    j=j+1

axis[1][0].scatter(x,y, c=kmeans.labels_)

print()
print("From cluster 2:")
print()
print("Accomodation Cost/Traveler Age")
print("The centroids of the 2 clusters are:")
print("{} {}".format(kmeans.cluster_centers_[0], kmeans.cluster_centers_[1]))
print("The radii are:")
print("{} {}".format(radii[0], radii[1]))
subsetss=split_data(subsets[1], kmeans.cluster_centers_, kmeans.labels_)
#print(subsets[0])
total=0
for i in subsets[1]:
    total=total+1
cluster1=0
for i in subsetss[0]:
    cluster1=cluster1+1
cluster2=0
for i in subsetss[1]:
    cluster2=cluster2+1
print("And the clusters have {} and {} data points out of the {} total points respectively".format(cluster1, cluster2, total))
print()
print("----------------------------------------------------------------------------------------")
#######################################################################################################  5
x=[]
y=[]
for i in subsets[1]:
    #x.append(pd.to_numeric(i[dataset_attributes().Accomodation_Cost])+pd.to_numeric(i[dataset_attributes().Transportation_Cost]))
    y.append(pd.to_numeric(i[dataset_attributes().Traveler_Age]))
    x.append(pd.to_numeric(i[dataset_attributes().Transportation_Cost]))
#plt.scatter(x,y)
subset=np.array(list(zip(x,y)))
#print(subset)

kmeans= KMeans(n_clusters=2, init='random', n_init='auto' , algorithm='lloyd').fit(subset) # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
radii=get_cluster_radii(kmeans.cluster_centers_, kmeans.labels_, subset)

#print(kmeans.cluster_centers_)
#print(kmeans.labels_)
#print(radii)
#print(data)

j=0
for i in kmeans.cluster_centers_:
    circle=plt.Circle(i, radii[j], color=cmap[j], fill=False)
    axis[1][1].add_patch(circle)
    j=j+1

axis[1][1].scatter(x,y, c=kmeans.labels_)

print()
print("From cluster 2:")
print()
print("Transfer Cost/Traveler Age")
print("The centroids of the 2 clusters are:")
print("{} {}".format(kmeans.cluster_centers_[0], kmeans.cluster_centers_[1]))
print("The radii are:")
print("{} {}".format(radii[0], radii[1]))
subsetss=split_data(subsets[1], kmeans.cluster_centers_, kmeans.labels_)
#print(subsets[0])
total=0
for i in subsets[1]:
    total=total+1
cluster1=0
for i in subsetss[0]:
    cluster1=cluster1+1
cluster2=0
for i in subsetss[1]:
    cluster2=cluster2+1
print("And the clusters have {} and {} data points out of the {} total points respectively".format(cluster1, cluster2, total))
print()
print("----------------------------------------------------------------------------------------")
#######################################################################################################
plt.show()
