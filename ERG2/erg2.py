# Παράδειγμα εξόδου μετά εκτέλεσης
"""

Traveler Age/Travel Duration
The centroids of the 2 clusters are:
[42.69230769  7.30769231] [29.3877551  7.7244898]
The radii are:
17.310427134359358 9.39179704467928
And the clusters have 39 and 98 data points out of the 137 total points respectively

----------------------------------------------------------------------------------------

From cluster 1:

Accomodation Cost/Travel Duration
The centroids of the 2 clusters are:
[1139.18918919    7.32432432] [5500.    7.]
The radii are:
1860.811565290628 1500.0
And the clusters have 37 and 2 data points out of the 39 total points respectively

----------------------------------------------------------------------------------------

From cluster 1:

Transportation Cost/Travel Duration
The centroids of the 2 clusters are:
[1733.33333333    7.83333333] [503.78787879   7.21212121]
The radii are:
1860.811565290628 1500.0
And the clusters have 6 and 33 data points out of the 39 total points respectively

----------------------------------------------------------------------------------------

From cluster 2:

Accomodation Cost/Traveler Age
The centroids of the 2 clusters are:
[874.23913043  29.40217391] [6166.66666667   29.16666667]
The radii are:
2125.7609076089725 1833.3346136359164
And the clusters have 92 and 6 data points out of the 98 total points respectively

----------------------------------------------------------------------------------------

From cluster 2:

Transfer Cost/Traveler Age
The centroids of the 2 clusters are:
[514.19354839  29.38709677] [2700.    29.4]
The radii are:
985.8093417454683 300.00426663632635
And the clusters have 93 and 5 data points out of the 98 total points respectively

----------------------------------------------------------------------------------------
"""
# Τα αποτελέσματα μπορεί να είναι διαφορετικά κάθε φορά λόγω των τυχαίων σημείων που επιλέγει ο kmeans

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
from sklearn.cluster import KMeans

class dataset_attributes:               # Για να κάνουμε την ανάθεση λίγο πιο εύκολη
    Travel_Duration=4
    Traveler_Age=6                      # Τα πεδία που είναι αριθμητικές τιμές είναι μόνο 4. 
    Accomodation_Cost=10
    Transportation_Cost=12

def safe_csv_read(csvstring):            #from python docs: https://docs.python.org/3/library/csv.html#examples
    output=[]
    with open(csvstring, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            output.append(row)
    return output

def eucledian_distance(point1,point2):     # Υπάρχει νομίζω μια συνάρτηση στην numpy αλλά έτσι βολεύομαι περισσότερο.
    return np.sqrt(np.sum(np.square(point1 - point2)))

def split_data(data,cluster_centers,labels):    # Με αυτή την συνάρτηση σπάμε τα δεδομένα από το κύριο pool σε μικρότερα pools ανάλογα σε ποιά συστάδα είναι
    output=[]
    for j in range(0, cluster_centers.shape[0]):    # Αρχικοποιούμε την ενδιάμεση λίστα για να έχουμε θέσεις όσες και ο αριθμός των συστάδων
        output.append([])
    k=0
    for i in data:                                  # Βάζουμε τα δεδομένα με βάση τον αριθμό συστάδας από την labels
        output[labels[k]].append(i)
        k=k+1
    return output

def get_cluster_radii(cluster_centers,labels,subset):
    output=np.zeros(cluster_centers.shape[0])               # Αρχηκοποίηση των λιστών. Η έξοδος θα είναι μεγέθους όσων είναι και οι συστάδες
    distances=np.zeros((cluster_centers.shape[0],subset.shape[0]))  # συστάδα επί πλήθος δεδομένων της
    spdat=split_data(subset, cluster_centers, labels)       #Κάνουμε το split
    spdatlen=[]

    for k in range(0,cluster_centers.shape[0]):
        j=0
        for i in spdat[k]:
            j=j+1
        spdatlen.append(j)
    for i in range (0,cluster_centers.shape[0]):
        for j in range(0,spdatlen[i]):
            distances[i][j]=eucledian_distance(spdat[i][j],  cluster_centers[i])    #Έτσι βρίσκουμε όλες τις αποστάσεις από το κάθε σημείο με το κάθε κέντρο στην συστάδα
    for i in labels:
        output[i]=np.amax(distances[i])
    return output
#######################################################################################################
data=safe_csv_read('source.csv')    # Μπορούσα να χρησιμοποιήσω pandas αλλά δεν με βόλευε ο τρόπος που διαβάζει τα csv
data.pop(0)                         # Αφαιρούμε τους τίτλους απο τα δεδομένα
cmap = { 0:'b',1:'y',2:'k',3:'g',4:'r' }    # Ένα color map 
fig, axis=plt.subplots(2, 3)        # Φτιάχνει τα subplots για να εμφανιστούν οι απεικονήσεις. Μια θέση περισεύει. Δεν μας ζητήσατε σχήμα. 
#######################################################################################################  1
x=[]
y=[]
for i in data:
    x.append(pd.to_numeric(i[dataset_attributes().Traveler_Age]))   #Εδώ απομονώνουμε τις στίλες με τις οποίες θέλουμε να κάνουμε τις συστάδες μας 
    y.append(pd.to_numeric(i[dataset_attributes().Travel_Duration]))    # Απλά τις παίρνουμε μια μια και μετά τις βάζουμε στο subset

subset=np.array(list(zip(x,y)))

kmeans= KMeans(n_clusters=2, init='random', n_init='auto').fit(subset) # https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
radii=get_cluster_radii(kmeans.cluster_centers_, kmeans.labels_, subset)        # Θέλουμε να έχουμε 2 clusters λόγω εκφώνησης, init="random" γιατί θέλουμε να είναι τυχαία τα αρχικά σημεία και δεν μας ενδιαφέρει.
                                                                                # Το n_init="auto" λέει πως θα γίνουν 10 επαναλήψεις σύμφωνα με τα docs

j=0
for i in kmeans.cluster_centers_:                                   # Είναι για τον κύκλο για να εμφανιστεί στο plot
    circle=plt.Circle(i, radii[j], color=cmap[j], fill=False)
    axis[0][0].add_patch(circle)
    j=j+1

axis[0][0].scatter(x,y, c=kmeans.labels_)   # Ανάθεση σε scatter subplot
print()
print("Traveler Age/Travel Duration")
print("The centroids of the 2 clusters are:")
print("{} {}".format(kmeans.cluster_centers_[0], kmeans.cluster_centers_[1]))
print("The radii are:")
print("{} {}".format(radii[0], radii[1]))
subsets=split_data(data, kmeans.cluster_centers_, kmeans.labels_)

total=0
for i in data:              # Τα data, subsets και subsetss (παρακάτω) είναι λίστες και δεν υπάρχει έτοιμη συνάρτηση για να δούμε το μέγεθός τους 
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
for i in subsets[0]:        #Στην ουσία το ίδιο με το πρώτο αλλά με τα στοιχεία της πρώτης συστάδας
    x.append(pd.to_numeric(i[dataset_attributes().Accomodation_Cost]))
    y.append(pd.to_numeric(i[dataset_attributes().Travel_Duration]))

subset=np.array(list(zip(x,y)))

kmeans= KMeans(n_clusters=2, init='random', n_init='auto' ).fit(subset)
radii=get_cluster_radii(kmeans.cluster_centers_, kmeans.labels_, subset)

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
for i in subsets[0]:    #Στην ουσία το ίδιο με το πρώτο αλλά με τα στοιχεία της πρώτης συστάδας
    x.append(pd.to_numeric(i[dataset_attributes().Transportation_Cost]))
    y.append(pd.to_numeric(i[dataset_attributes().Travel_Duration]))
subset=np.array(list(zip(x,y)))

kmeans= KMeans(n_clusters=2, init='random', n_init='auto' ).fit(subset) 

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
for i in subsets[1]:    #Στην ουσία το ίδιο με το πρώτο αλλά με τα στοιχεία της δεύτερης συστάδας
    y.append(pd.to_numeric(i[dataset_attributes().Traveler_Age]))
    x.append(pd.to_numeric(i[dataset_attributes().Accomodation_Cost]))

subset=np.array(list(zip(x,y)))

kmeans= KMeans(n_clusters=2, init='random', n_init='auto' ).fit(subset) 
radii=get_cluster_radii(kmeans.cluster_centers_, kmeans.labels_, subset)

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
for i in subsets[1]:    #Στην ουσία το ίδιο με το πρώτο αλλά με τα στοιχεία της δεύτερης συστάδας
    y.append(pd.to_numeric(i[dataset_attributes().Traveler_Age]))
    x.append(pd.to_numeric(i[dataset_attributes().Transportation_Cost]))

subset=np.array(list(zip(x,y)))

kmeans= KMeans(n_clusters=2, init='random', n_init='auto' ).fit(subset) 
radii=get_cluster_radii(kmeans.cluster_centers_, kmeans.labels_, subset)

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
