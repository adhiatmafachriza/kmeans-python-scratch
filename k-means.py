import matplotlib.pyplot as plt
import pandas as pd
import random
import math

customers = pd.read_csv(r'D:\Data F\Kuliah\Data Science\Datasets\mall customers\Mall_Customers.csv')
# featureX = [1, 1, 2, 4, 4, 5]
# featureY = [1, 2, 2, 3, 5, 4]
featureX = customers['Annual Income (k$)']
featureY = customers['Spending Score (1-100)']

# kmeans class
class KMeans:
    def __init__(self):
        self.clusters = []


    def exit(self):
        count = 0

        # cek apakah posisi centroid berubah
        for cluster in self.clusters:
            if cluster.centroidPosition['positionX'] == cluster.centroidPosition['lastPosX']:
                if cluster.centroidPosition['positionY'] == cluster.centroidPosition['lastPosY']:
                    count += 1
        
        if count == len(self.clusters):
            return True
        else:
            return False
    

    def clearClusterMembers(self):
        for cluster in self.clusters:
            cluster.members['memberX'].clear()
            cluster.members['memberY'].clear()


# cluster class
class Cluster:
    def __init__(self):
        self.centroidPosition = {
            'positionX': random.randint(1, round(max(featureX))),
            'positionY': random.randint(1, round(max(featureY))),
            'lastPosX': None,
            'lastPosY': None
        }
        self.members = {
            'memberX': [],
            'memberY': []
        }
        self.distance = {
            'distanceX': [],
            'distanceY': [],
            'distanceTotal': []
        }
    

    def euclidianDistance(self):
        global featureX
        global featureY

        # mengukur jarak data ke centroid 1 pada sumbu x
        for data in featureX:
            distance = pow((self.centroidPosition['positionX'] - data), 2)
            self.distance['distanceX'].append(distance)

        # mengukur jarak data ke centroid 1 pada sumbu y
        for data in featureY:
            distance = pow((self.centroidPosition['positionY'] - data), 2)
            self.distance['distanceY'].append(distance)

        # mengukur jarak keseluruhan
        for i in range(0, len(featureX)):
            distanceTotal = math.sqrt(self.distance['distanceX'][i] + self.distance['distanceY'][i])
            self.distance['distanceTotal'].append(distanceTotal)
        
    
    def updateCentroidPos(self):
        avgDistanceX = 0
        avgDistanceY = 0

        if len(self.members['memberX']) == 0:
            avgDistanceX = 0
            avgDistanceY = 0
        else:
            for i in range(0, len(self.members['memberX'])):
                avgDistanceX += self.members['memberX'][i]
                avgDistanceY += self.members['memberY'][i]
            
            avgDistanceX = avgDistanceX / len(self.members['memberX'])
            avgDistanceY = avgDistanceY / len(self.members['memberY'])

        # simpan posisi lama centroid
        self.centroidPosition['lastPosX'] = self.centroidPosition['positionX']
        self.centroidPosition['lastPosY'] = self.centroidPosition['positionY']
        # update posisi centroid
        self.centroidPosition['positionX'] = avgDistanceX
        self.centroidPosition['positionY'] = avgDistanceY


if __name__ == '__main__':
    print('===== K-MEANS CLUSTERING =====')
    totalClusters = int(input('Jumlah cluster = '))
    iter = 0

    # init
    kmeans = KMeans()
    for i in range(0, totalClusters):
        kmeans.clusters.append(Cluster())

    # ITERASI
    while(True):
        iter += 1
        # ukur jarak
        for cluster in kmeans.clusters:
            cluster.euclidianDistance()

        # bandingkan jarak setiap data dan centroid, lalu masukkan kedalam cluster
        for i in range(0, len(featureX)):
            kmeans.clusters.sort(key=lambda cluster: cluster.distance['distanceTotal'][i])
            kmeans.clusters[0].members['memberX'].append(featureX[i])
            kmeans.clusters[0].members['memberY'].append(featureY[i])

        # update posisi centroid
        for cluster in kmeans.clusters:
            cluster.updateCentroidPos()

        # posisi semua centroid tidak berubah?
        if(kmeans.exit() == True):
            break
        else:
            kmeans.clearClusterMembers()

    # visualisasi scatter plot
    for cluster in kmeans.clusters:
        plt.scatter(cluster.members['memberX'], cluster.members['memberY'])
    plt.show()