import json, os
import random
import cv2
import numpy as np
import pandas as pd

import tensorflow as tf
from keras import backend as K

from tensorflow.keras.utils import Sequence
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Input, Flatten
from tensorflow.keras.layers import GlobalAveragePooling2D, BatchNormalization
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications import MobileNet
from tensorflow.keras.applications import VGG16
from tensorflow.keras.applications import VGG19
from tensorflow.keras.applications import InceptionResNetV2
from tensorflow.keras.applications import ResNet50
from tensorflow.keras import optimizers, utils
from tensorflow.keras import regularizers
from tensorflow.keras.callbacks import ReduceLROnPlateau

from tensorflow.keras.preprocessing.image import ImageDataGenerator

class DataSequence(Sequence):
    def __init__(self, data_path, label):
        self.batch = 4
        self.data_file_path = data_path
        self.datagen = ImageDataGenerator(
                            rotation_range=30,
                            width_shift_range=0.2,
                            height_shift_range=0.2,
                            zoom_range=0.5
                        )
        d_list = os.listdir(self.data_file_path)
        self.f_list = []
        for dir in d_list:
            if dir == 'empty': continue
            for f in os.listdir(self.data_file_path+'/'+dir):
                self.f_list.append(self.data_file_path+'/'+dir+'/'+f)
        self.label = label
        self.length = len(self.f_list)

    def __getitem__(self, idx):
        warp = self.batch
        aug_time = 3
        datas, labels = [], []
        label_dict = self.label

        for f in random.sample(self.f_list, warp):
            img = cv2.imread(f)
            img = cv2.resize(img, (224, 224))
            img = img.astype(np.float32) / 255.0
            datas.append(img)
            label = f.split('/')[2].split('_')[-1]
            labels.append(label_dict[label])
            # Augmentation image
            for num in range(aug_time):
                tmp = self.datagen.random_transform(img)
                datas.append(tmp)
                labels.append(label_dict[label])

        datas = np.asarray(datas)
        labels = pd.DataFrame(labels)
        labels = utils.to_categorical(labels, len(label_dict))
        return datas, labels

    def __len__(self):
        return self.length

    def on_epoch_end(self):
        ''' 何もしない'''
        pass

def categorical_focal_loss(gamma=2., alpha=.25):
    """
    Softmax version of focal loss.
           m
      FL = ∑  -alpha * (1 - p_o,c)^gamma * y_o,c * log(p_o,c)
          c=1
      where m = number of classes, c = class and o = observation
    Parameters:
      alpha -- the same as weighing factor in balanced cross entropy
      gamma -- focusing parameter for modulating factor (1-p)
    Default value:
      gamma -- 2.0 as mentioned in the paper
      alpha -- 0.25 as mentioned in the paper
    References:
        Official paper: https://arxiv.org/pdf/1708.02002.pdf
        https://www.tensorflow.org/api_docs/python/tf/keras/backend/categorical_crossentropy
    Usage:
     model.compile(loss=[categorical_focal_loss(alpha=.25, gamma=2)], metrics=["accuracy"], optimizer=adam)
    """
    def categorical_focal_loss_fixed(y_true, y_pred):
        """
        :param y_true: A tensor of the same shape as `y_pred`
        :param y_pred: A tensor resulting from a softmax
        :return: Output tensor.
        """

        # Scale predictions so that the class probas of each sample sum to 1
        y_pred /= K.sum(y_pred, axis=-1, keepdims=True)

        # Clip the prediction value to prevent NaN's and Inf's
        epsilon = K.epsilon()
        y_pred = K.clip(y_pred, epsilon, 1. - epsilon)

        # Calculate Cross Entropy
        cross_entropy = -y_true * K.log(y_pred)

        # Calculate Focal Loss
        loss = alpha * K.pow(1 - y_pred, gamma) * cross_entropy

        # Sum the losses in mini_batch
        return K.sum(loss, axis=1)

    return categorical_focal_loss_fixed

class CustumModel():
    def __init__(self):
        shape = (224, 224, 3)
        input_tensor = Input(shape=shape)

        '''
        学習済みモデルのロード(base_model)
        '''
        # self.base_model = VGG16(weights='imagenet', include_top=False, input_tensor=input_tensor)
        # self.base_model = VGG19(weights='imagenet', include_top=False, input_tensor=input_tensor)
        # self.base_model = MobileNet(weights='imagenet', include_top=False, input_tensor=input_tensor)
        self.base_model = ResNet50(weights='imagenet', include_top=False, input_tensor=input_tensor)

    def createModel(self, label_dict):
        '''
        転移学習用のレイヤーを追加
        '''
        added_layer = GlobalAveragePooling2D()(self.base_model.output)
        added_layer = Dense(256)(added_layer)
        added_layer = BatchNormalization()(added_layer)
        added_layer = Activation('relu')(added_layer)
        added_layer = Dense(len(label_dict), activation='softmax', name='classification')(added_layer)

        '''
        base_modelと転移学習用レイヤーを結合
        '''
        model = Model(inputs=self.base_model.input, outputs=added_layer)

        '''
        base_modelのモデルパラメタは学習させない。
        (added_layerのモデルパラメタだけを学習させる)
        '''
        for layer in self.base_model.layers[:-4]:
            layer.trainable = False
        model.summary()

        return model


if __name__=="__main__":
    '''
    学習用画像のロード
    '''
    label_dict = {}
    count = 0
    for d_name in os.listdir('./train'):
        if d_name == 'empty': continue
        if d_name == '.DS_Store': continue
        d_name = d_name.split('_')[-1]
        label_dict[d_name] = count
        count += 1
    train_gen = DataSequence('./train', label_dict)

    cm = CustumModel()
    model = cm.createModel(label_dict)

    callbacks = [
        ReduceLROnPlateau(monitor='loss', factor=0.1, patience=10, min_lr=1e-6)
    ]

    '''
    全体のモデルをコンパイル
    '''
    opt = optimizers.Adam(lr=1e-4)
    # opt = optimizers.SGD(lr=1e-4)
    model.compile(optimizer=opt, loss=[categorical_focal_loss(alpha=.25, gamma=2)], metrics=['accuracy'])
    # model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])

    '''
    モデルの学習
    '''
    model.fit_generator(
         train_gen,
         epochs=10,
         steps_per_epoch=int(train_gen.length),
         callbacks=callbacks,
         validation_data=train_gen,
         validation_steps=int(train_gen.length / 10),
    )

    '''
    モデルパラメタの保存
    '''
    model.save('./model/custum_resnet.h5')

    '''
    ラベル情報を保存
    '''
    l_dict = {label_dict[name]: name for name in label_dict.keys()}
    json.dump(l_dict, open('./model/labels.json', 'w'), indent=4)
