import cv2
import os
import shutil
import cnn_app

input_path = "data/cat.jpg"
output_path = "data/result.jpg"
outbouns_path = "data/bouns.csv"
cascade_path = "data/cascade.xml"
catface_path = "data/catface/"

#ディレクトリが既にある場合は消す
if os.path.exists(catface_path):
    shutil.rmtree(catface_path)
os.mkdir(catface_path)

if os.path.exists(outbouns_path) :
    os.remove(outbouns_path)

img = cv2.imread(input_path)
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cascade = cv2.CascadeClassifier(cascade_path)
catface = cascade.detectMultiScale(img_g, scaleFactor=1.1, minSize=(20, 20))

count = 0

if len(catface) != 0 :
    for i in catface :
        cv2.imwrite(catface_path + str(count) + ".jpg", img[i[1]:i[1]+i[3], i[0]:i[0]+i[2]])
        cv2.rectangle(img, (i[0], i[1]), (i[0] + i[2], i[1] + i[3]), (255, 255, 255), thickness=10)
        result_str = str(count) + "\n" + str(i[0]) + "," + str(i[1])  + "," + str(i[2]) + "," + str(i[3]) + "\n"
        with open(outbouns_path, mode='a') as f:
            f.write(result_str)
        count+=1
    cv2.imwrite(output_path, img)

    feel = cnn_app.catface_feeling()
    with open(outbouns_path, mode='a') as f:
        f.write(str(feel))
    f.close()

