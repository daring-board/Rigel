from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from keras.layers import Dense, Input, concatenate
from keras.layers import Conv2D, Flatten, Lambda
from keras.layers import Reshape, Conv2DTranspose
from keras.models import Model
from keras.datasets import mnist
from keras.losses import mse, binary_crossentropy
from keras.utils import np_utils   ### 追加
from keras import backend as K
from keras.preprocessing.image import array_to_img, img_to_array, load_img  ###　追加
from sklearn.model_selection import train_test_split  ### 追加

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import random

def sampling(args):
    z_mean, z_log_var = args
    batch = K.shape(z_mean)[0]
    dim = K.int_shape(z_mean)[1]
    epsilon = K.random_normal(shape=(batch, dim))
    return z_mean + K.exp(0.5 * z_log_var) * epsilon

def save_imgs(encoder, decoder, d_path_dict, num, idx):
    r, c = 3, 3

    x, y, label = [], [], []
    d_path = d_path_dict[num]
    for picture in random.sample(os.listdir(d_path), 2 * 2):
        img = img_to_array(load_img(d_path+picture, target_size=(224, 224)))  
        x.append(img)
        label.append(abs(num-1))
    x = np.asarray(x)
    y = np.asarray(label)
    
    x = x.astype('float32')
    x = x / 255.0
    y = np_utils.to_categorical(y, len(d_path_dict))

    vec = encoder.predict([x, y])[2]
    vecs = np.asarray(vecs)
    
    [label.append(abs(num-1)) for _ in range(5)]
    y = np.asarray(label)
    y = np_utils.to_categorical(y, len(d_path_dict))
    
    imgs = decoder.predict([vecs, y])
    fig, axs = plt.subplots(r, c)
    cnt = 0
    for i in range(r):
        for j in range(c):
            axs[i,j].imshow(imgs[cnt])
            axs[i,j].axis('off')
            cnt += 1
    fig.savefig("images/imgs%d_%d.png"%(idx, num))
    plt.close()

def save_imgs_X(encoder, decoder, d_path_dict, epoch):
    r, c = 2, 6

    x, y, label = [], [], []
    for k in d_path_dict.keys():
        d_path = d_path_dict[k]
        for picture in random.sample(os.listdir(d_path), 2):
            img = img_to_array(load_img(d_path+picture, target_size=(224, 224)))  
            x.append(img)
            label.append(k)
    x = np.asarray(x)
    y = np.asarray(label)
    
    x = x.astype('float32')
    x = x / 255.0
    y = np_utils.to_categorical(y, len(d_path_dict))

    vec = encoder.predict([x, y])[2]
    vecs, label = [], []
    unit = 1 / (c - 2)
    for idy in range(0, 4, 2):
        vecs.append(vec[idy + 1])
        label.append([0, 1])
        for idx in range(c - 2):
            tmp = unit * idx * vec[idy] + (1 - unit * idx) * vec[idy + 1]
            vecs.append(tmp)
            label.append(np.asarray([unit * idx, (1 - unit * idx)]))
        vecs.append(vec[idy])
        label.append([1, 0])
    vecs = np.asarray(vecs)
    y = np.asarray(label)
    print(vecs.shape)
    print(y.shape)
    
    imgs = decoder.predict([vecs, y])
    fig = plt.figure(figsize=(16, 8))
    axs = fig.subplots(r, c)
    cnt = 0
    for i in range(r):
        for j in range(c):
            axs[i,j].imshow(imgs[cnt])
            axs[i,j].axis('off')
            cnt += 1
    fig.savefig("images/imgs%d.png"%epoch)
    plt.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    help_ = "Load h5 model trained weights"
    parser.add_argument("-w", "--weights", help=help_)
    help_ = "Use mse loss instead of binary cross entropy (default)"
    parser.add_argument("-m", "--mse", help=help_, action='store_true')
    args = parser.parse_args()


    ### daterset
    data = []
    y = []

    d_path_dict = {
        0: './transfar/cgan/chunli/trainA/',
        1: './transfar/cgan/chunli/trainB/',
        # 1: './transfar/style/pink/',
        # 1: './transfar/cgan/chunli/trainC/'
    }
        
    for k in d_path_dict.keys():
        d_path = d_path_dict[k]
        for picture in os.listdir(d_path):
            img = img_to_array(load_img(d_path+picture, target_size=(224, 224)))  
            data.append(img)
            y.append(k)

    data = np.asarray(data)
    y = np.asarray(y)
    
    data = data.astype('float32')
    data = data / 255.0
    y = np_utils.to_categorical(y, len(d_path_dict))
    
    image_size = 224
    input_shape = data.shape[1:]
    batch_size = 4
    kernel_size = 3
    filters = 32
    latent_dim = 100

    # VAE model = encoder + decoder
    # build encoder model
    inputs1 = Input(shape=input_shape, name='encoder_input')
    inputs2 = Input(shape=y.shape[1:], name='label')
    x = inputs1
    for i in range(3):
        filters *= 2    
        x = Conv2D(filters=filters,
                kernel_size=kernel_size,
                activation='relu',
                strides=2,
                padding='same')(x)

    # shape info needed to build decoder model
    shape = K.int_shape(x)

    # generate latent vector Q(z|X)
    x = Flatten()(x)
    x = concatenate([x, inputs2])
    x = Dense(512, activation='relu')(x)
    z_mean = Dense(latent_dim, name='z_mean')(x)
    z_log_var = Dense(latent_dim, name='z_log_var')(x)

    # use reparameterization trick to push the sampling out as input
    # note that "output_shape" isn't necessary with the TensorFlow backend
    z = Lambda(sampling, output_shape=(latent_dim,), name='z')([z_mean, z_log_var])

    # instantiate encoder model
    encoder = Model(inputs=[inputs1, inputs2], outputs=[z_mean, z_log_var, z], name='encoder')
    encoder.summary()

    # build decoder model
    latent_inputs = Input(shape=(latent_dim,), name='z_sampling')
    x = concatenate([latent_inputs, inputs2])
    x = Dense(shape[1] * shape[2] * shape[3], activation='relu')(x)
    x = Reshape((shape[1], shape[2], shape[3]))(x)

    for i in range(3):
        x = Conv2DTranspose(filters=filters,
                            kernel_size=kernel_size,
                            activation='relu',
                            strides=2,
                            padding='same')(x)
        filters //= 2

    outputs = Conv2DTranspose(filters=3,
                            kernel_size=kernel_size,
                            activation='sigmoid',
                            padding='same',
                            name='decoder_output')(x)

    # instantiate decoder model
    decoder = Model([latent_inputs, inputs2], outputs, name='decoder')
    decoder.summary()


    # instantiate VAE model
    outputs = decoder([encoder([inputs1, inputs2])[2], inputs2])
    vae = Model([inputs1, inputs2], outputs, name='vae')

    # VAE loss = mse_loss or xent_loss + kl_loss
    if args.mse:
        reconstruction_loss = mse(K.flatten(inputs1), K.flatten(outputs))
    else:
        reconstruction_loss = binary_crossentropy(K.flatten(inputs1), K.flatten(outputs))

    reconstruction_loss *= image_size * image_size
    kl_loss = 1 + z_log_var - K.square(z_mean) - K.exp(z_log_var)
    kl_loss = K.sum(kl_loss, axis=-1)
    kl_loss *= -0.5
    vae_loss = K.mean(reconstruction_loss + kl_loss)
    vae.add_loss(vae_loss)
    vae.compile(optimizer='rmsprop')
    vae.summary()

    if args.weights:
        vae.load_weights(args.weights)
        save_imgs(encoder, decoder, d_path)
    else:
        epochs = 10
        for idx in range(1, 51):
            x_train, x_test, y_train, y_test = train_test_split(data, y, test_size=0.1)
            vae.fit([x_train, y_train], epochs=epochs, batch_size=batch_size, validation_data=([x_test, y_test], None))
            vae.save_weights('./model/vae_cnn_%d.h5'%idx)
            save_imgs_X(encoder, decoder, d_path_dict, idx)
            # for k in d_path_dict.keys():
            #     save_imgs(encoder, decoder, d_path_dict, k, idx)

    
