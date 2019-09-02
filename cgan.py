from __future__ import print_function, division

from keras.layers import Input, Dense, Reshape, Flatten, Dropout, Conv2DTranspose
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.models import Sequential, Model
from keras.initializers import RandomNormal
from keras.optimizers import Adam, SGD, RMSprop
from keras import metrics
import keras.backend as K
import matplotlib.pyplot as plt
from numpy.random import randn, random, choice
import sys
import numpy as np
import pickle
import img_processing as ip

def custum_acc(y_true, y_pred):
    y_true = K.round(y_true)
    return metrics.binary_accuracy(y_true, y_pred)

class DCGAN():
    def __init__(self):
        # Input shape
        self.img_rows = 224
        self.img_cols = 224
        self.channels = 3
        self.img_shape = (self.img_rows, self.img_cols, self.channels)
        self.latent_dim = 512

        optimizer = Adam(lr=0.0002, beta_1=0.5)
        # optimizer = RMSprop(lr=1e-4)
        # optimizer = SGD(lr=1e-2)


        # Build and compile the discriminator
        self.discriminator = self.build_discriminator()
        self.discriminator.compile(loss='binary_crossentropy',
            optimizer=optimizer,
            metrics=[custum_acc])

        # Build the generator
        self.generator = self.build_generator()

        # The generator takes noise as input and generates imgs
        z = Input(shape=(self.latent_dim,))
        img = self.generator(z)

        # For the combined model we will only train the generator
        self.discriminator.trainable = False

        # The discriminator takes generated images as input and determines validity
        valid = self.discriminator(img)

        # The combined model  (stacked generator and discriminator)
        # Trains the generator to fool the discriminator
        self.combined = Model(z, valid)
        # optimizer = RMSprop(lr=1e-2)
        # optimizer =  Adam(lr=1e-2, beta_1=0.5)
        self.combined.compile(loss='binary_crossentropy', optimizer=optimizer)

    def build_generator(self):
        init = RandomNormal(mean=0.0, stddev=0.02)

        model = Sequential()

        model.add(Dense(512 * 7 * 7, activation="relu", kernel_initializer=init, input_dim=self.latent_dim))
        model.add(Reshape((7, 7, 512)))
        model.add(Conv2DTranspose(256, kernel_size=3, strides=2, padding='same'))
        model.add(BatchNormalization())
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2DTranspose(128, kernel_size=3, strides=2, padding='same'))
        model.add(BatchNormalization())
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2DTranspose(64, kernel_size=3, strides=2, padding='same'))
        model.add(BatchNormalization())
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2DTranspose(32, kernel_size=3, strides=2, padding='same'))
        model.add(BatchNormalization())
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2DTranspose(3, kernel_size=3, strides=2, padding='same'))
        model.add(Activation("tanh"))

        model.summary()

        noise = Input(shape=(self.latent_dim,))
        img = model(noise)

        return Model(noise, img)

    def build_discriminator(self):

        model = Sequential()

        model.add(Conv2D(8, kernel_size=3, strides=2, input_shape=self.img_shape, padding="same"))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2D(16, kernel_size=3, strides=2, padding="same"))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2D(32, kernel_size=3, strides=2, padding="same"))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Conv2D(64, kernel_size=3, strides=1, padding="same"))
        model.add(LeakyReLU(alpha=0.2))
        model.add(Flatten())
        model.add(Dense(1, activation='sigmoid'))

        model.summary()

        img = Input(shape=self.img_shape)
        validity = model(img)

        return Model(img, validity)

    '''
    https://machinelearningmastery.com/how-to-code-generative-adversarial-network-hacks/
    '''
    def generate_latent_points(self, latent_dim, n_samples):
        # generate points in the latent space
        x_input = randn(latent_dim * n_samples)
        # reshape into a batch of inputs for the network
        x_input = x_input.reshape((n_samples, latent_dim))
        return x_input

    def smooth_positive_labels(self, y):
    	return y - 0.4 + (random(y.shape) * 0.6)

    def smooth_negative_labels(self, y):
        return y + random(y.shape) * 0.3

    def noisy_labels(self, y, p_flip):
        # determine the number of labels to flip
        n_select = int(p_flip * y.shape[0])
        # choose labels to flip
        flip_ix = choice([i for i in range(y.shape[0])], size=n_select)
        # invert the labels in place
        y[flip_ix] = 1 - y[flip_ix]
        return y

    def train(self, epochs, batch_size=128, save_interval=50):

        # Load the dataset
        X_train, f_list = ip.process('./transfar/cgan/chunli/trainB/', switch=True)
        X_train = np.asarray(X_train)

        # Adversarial ground truths
        valid_disc = self.smooth_positive_labels(self.noisy_labels(np.ones((batch_size, 1)), 0.05))
        valid_gene = np.ones((batch_size, 1))
        fake_disc = self.smooth_negative_labels(self.noisy_labels(np.zeros((batch_size, 1)), 0.05))

        for epoch in range(epochs):

            # Select a random half of images
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]

            # Sample noise and generate a batch of new images
            noise = self.generate_latent_points(self.latent_dim, batch_size)
            # noise = np.random.normal(0, 1, (batch_size, self.latent_dim))
            gen_imgs = self.generator.predict(noise)

            # Train the discriminator (real classified as ones and generated as zeros)
            d_loss_real = self.discriminator.train_on_batch(imgs, valid_disc)
            d_loss_fake = self.discriminator.train_on_batch(gen_imgs, fake_disc)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fake)

            # Train the generator (wants discriminator to mistake images as real)
            g_loss = self.combined.train_on_batch(noise, valid_gene)

            # Plot the progress
            print ("%d [D loss: %f, acc.: %.2f%%] [G loss: %f]" % (epoch, d_loss[0], 100*d_loss[1], g_loss))

            # If at save interval => save generated image samples
            if epoch % save_interval == 0:
                self.save_imgs(epoch)

    def save_imgs(self, epoch):
        r, c = 5, 5
        noise = self.generate_latent_points(self.latent_dim, r*c)
        # noise = np.random.normal(0, 1, (r * c, self.latent_dim))
        gen_imgs = self.generator.predict(noise)
        gen_imgs = 0.5 * gen_imgs + 0.5

        fig, axs = plt.subplots(r, c)
        cnt = 0
        for i in range(r):
            for j in range(c):
                axs[i,j].imshow(gen_imgs[cnt, :,:,:])
                axs[i,j].axis('off')
                cnt += 1
        fig.savefig("images/img_%d.png" % epoch)
        plt.close()

if __name__ == '__main__':
    dcgan = DCGAN()
    dcgan.train(epochs=50000, batch_size=40, save_interval=200)
