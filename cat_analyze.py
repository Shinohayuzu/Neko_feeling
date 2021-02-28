import cv2
import os
import shutil
import cnn_app
from PIL import Image, ImageFont, ImageDraw
import numpy as np

input_path = "data/cat.jpg"
output_path = "data/result.jpg"
cascade_path = "data/cascade.xml"
catface_path = "data/catface/"

#テキスト描画関数
def textDraw(img, text, pos) :
    font=ImageFont.truetype("C:\Windows\Fonts\meiryo.ttc", 32)
    img = Image.fromarray(img)
    draw = ImageDraw.Draw(img)
    #テキスト描画
    draw.text(pos, text, font=font, fill=(255, 255, 255, 0))
    img = np.array(img)
    return img

#ディレクトリが既にある場合は消す
if os.path.exists(catface_path):
    shutil.rmtree(catface_path)
os.mkdir(catface_path)

img = cv2.imread(input_path)
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#ねこ顔検出
cascade = cv2.CascadeClassifier(cascade_path)
catface = cascade.detectMultiScale(img_g, scaleFactor=1.1, minSize=(20, 20))

count = 0
pos = []

#表情分析にかけて結果画像を生成
if len(catface) != 0 :
    for i in catface :
        cv2.imwrite(catface_path + str(count) + ".jpg", img[i[1]:i[1]+i[3], i[0]:i[0]+i[2]])
        cv2.rectangle(img, (i[0], i[1]), (i[0] + i[2], i[1] + i[3]), (255, 255, 255), thickness=10)
        pos.append([i[0], i[1]+i[3]])
        count+=1
    #表情分析
    feel = cnn_app.catface_feeling()
    #テキスト描画
    for j in range(len(feel)):
        img = textDraw(img, feel[j], pos[j])
    cv2.imwrite(output_path, img)

