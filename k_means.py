import os
import glob
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image
from sklearn.decomposition import IncrementalPCA
from sklearn.cluster import KMeans

from pyclustering.cluster.xmeans import xmeans, kmeans_plusplus_initializer
from pyclustering.utils import draw_clusters

np.random.seed(5)

read_Path = glob.glob('cats_face/all/*')
out_Path = '/output'
print('ねこちゃんの数:', len(read_Path))

img_list = []

for file in read_Path :
    img = cv2.imread(file)
    img = cv2.resize(img, (128,128), cv2.INTER_AREA)
    img_list.append(img)

cats = np.array(img_list)
cats = cats.reshape(cats.shape[0], -1)

n_clusters = 8
kmeans = KMeans(n_clusters=n_clusters, random_state=5).fit(cats)
labels = kmeans.labels_
print("K-means clustering done.")

for i in range(n_clusters):
    label = np.where(labels==i)[0]
    os.mkdir(('output/' + str(i)))
    # Image placing
    for j in label:
        img = cv2.imread(read_Path[j])
        out_Path = "output/" + str(i) + "/" + str(j) + ".jpg"
        cv2.imwrite(out_Path, img)
print("Image placing done.")