import os
import glob
import cv2
import numpy as np
import matplotlib as plt
import keras
from keras.utils.np_utils import to_categorical
from keras.layers import Dense, Dropout, Flatten, Input
from keras.applications.vgg16 import VGG16
from keras.models import Model, Sequential
from keras import optimizers
from keras.callbacks import EarlyStopping, TensorBoard, ModelCheckpoint
keras.backend.clear_session()
import tensorflow as tf

#ねこ気持ちのリスト
catfeel_list = ["akubi", "bikkuri", "kininaru", "magao", "metoji", "nemui", "pero"]
print(catfeel_list)

#ファイル取得
def getPath(feel) :
    read_path="cats_face/"+feel+'/*'
    path = glob.glob(read_path)
    return path

#画像配列
def getImgArray(feel) :
    path = getPath(feel)
    print(path)
    img_feel = []
    for i in range(len(path)) :
        img = cv2.imread(path[i])
        img_feel.append(img)
    return img_feel

#画像のラベル付と分割
X = []
Y = []
for feel in range(len(catfeel_list)) :
    print(catfeel_list[feel] + ":" + str(len(getImgArray(catfeel_list[feel]))))
    X += getImgArray(catfeel_list[feel])
    Y += [feel] * len(getImgArray(catfeel_list[feel]))
X = np.array(X)
Y = np.array(Y)

rand_index = np.random.permutation(np.arange(len(X)))
X = X[rand_index]
Y = Y[rand_index]

X_train = X[:int(len(X)*0.8)]
Y_train = Y[:int(len(Y)*0.8)]
X_test = X[int(len(X)*0.8):]
Y_test = Y[int(len(X)*0.8):]

Y_train = to_categorical(Y_train)
Y_test = to_categorical(Y_test)

#学習
vgg16 = VGG16(include_top=False, weights='imagenet', input_tensor=Input(shape=(128, 150, 3)))

top_model = Sequential()
top_model.add(Flatten(input_shape=vgg16.output_shape[1:]))
top_model.add(Dense(512, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(len(catfeel_list), activation='softmax'))

model = Model(inputs=vgg16.input, outputs=top_model(vgg16.output))
for layer in model.layers[:15] :
    layer.trainable = False

model.compile(loss='categorical_crossentropy', optimizer=optimizers.SGD(lr=1e-4, momentum=0.9), metrics = ['accuracy'])

X_train = tf.ragged.constant(X_train)
Y_train = tf.ragged.constant(Y_train)
X_test = tf.ragged.constant(X_test)
Y_test = tf.ragged.constant(Y_test)

model.summary()
es_cb = EarlyStopping(monitor='val_loss', patience=2, verbose=1, mode='auto')
tb_cb = TensorBoard(log_dir="tensorlog", histogram_freq=1)
history = model.fit(X_train, Y_train, batch_size=150, epochs=20, verbose=1, validation_data=(X_test, Y_test), callbacks=[es_cb, tb_cb])

model.save("model.h5")

scores = model.evaluate(X_test, Y_test, verbose=1)
print("Test loss:", scores[0])
print("Test accuracy:", scores[1])

plt.plot(history.history['acc'], label='acc', ls='-')
plt.plot(history.history['val_acc'], label='val_acc', ls='-')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(loc='best')
plt.show()