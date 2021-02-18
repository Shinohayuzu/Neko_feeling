import sys
import cv2
import glob
import os

#Cat Face Cut

#Cat Face Detect
def detect_cat(flame, cascade_cat):
    CAT_FLAG=0
    image = flame
    if image is None:
        print('cannot open image')
        sys.exit(-1)
    image_cat = flame.copy()
    cascade = cv2.CascadeClassifier(cascade_cat)
    if cascade.empty():
        print('cannot load cascade')
        sys.exit(-1)
    cat = cascade.detectMultiScale(image, 1.1, 3)
    cat_face = image_cat
    for (x, y, w, h) in cat:
        print(x, y, w, h)
        #cv2.rectangle(image_cat, (x, y), (x+w, y+h), (0, 0, 255), 2)
        cat_face = image_cat[y:y+h, x:x+w]
        CAT_FLAG = 1
    return cat_face, CAT_FLAG


k=0

#ファイル名取得
files=[]
files.append(glob.glob("cats/*"))
files.append(glob.glob("cats_2/*"))
files.append(glob.glob("cats_3/*"))

cascade = "cascade.xml"

for i in range(3):
    for file in files[i]:
        print(file)
        cat_flame = cv2.imread(file)
        result, FLAG = detect_cat(cat_flame, cascade)
        if FLAG == 1 :
            r_img = cv2.resize(result, (256, 256))
            resultPath = 'cats_face/' + str(k) + '.jpg'
            print(resultPath)
            cv2.imwrite(resultPath, result)
        else :
            out_Path = 'misc/' + str(k) + '.jpg'
            cv2.imwrite(out_Path, result)
            os.remove(file)
        k+=1
