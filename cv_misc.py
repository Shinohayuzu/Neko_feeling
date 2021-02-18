import cv2
import glob
import os

read_Path = glob.glob("cats_3/*")
i=951

for file in read_Path :
    img = cv2.imread(file)
    out_Path = 'all/' + str(i) + '.jpg'
    print(file)
    print(out_Path)
    cv2.imwrite(out_Path, img)
    i+=1

