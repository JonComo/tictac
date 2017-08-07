import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras import backend as K
from keras.callbacks import ModelCheckpoint
from keras.models import model_from_json

import numpy as np

import json

class Detector():
    def __init__(self, img_rows, img_cols, weights_path):
        self.img_rows = img_rows
        self.img_cols = img_cols
        self.create_model(img_rows, img_cols)

        print('loading model weights from path: {}'.format(weights_path))
        self.model.load_weights(weights_path, by_name=False)
        print('loaded weights')

    def create_model(self, img_rows, img_cols):
        num_outputs = 18

        if K.image_data_format() == 'channels_first':
            self.input_shape = (1, img_rows, img_cols)
        else:
            self.input_shape = (img_rows, img_cols, 1)

        self.model = Sequential()
        self.model.add(Conv2D(32, kernel_size=(6, 6),
                        activation='relu',
                        input_shape=self.input_shape, 
                        strides=(1, 1)))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(16, kernel_size=(4, 4), 
                        activation='relu'))
        self.model.add(MaxPooling2D(pool_size=(2, 2)))
        self.model.add(Conv2D(16, kernel_size=(2, 4), 
                        activation='relu'))
        self.model.add(Dropout(0.15))
        self.model.add(Flatten())
        self.model.add(Dense(256, activation='sigmoid'))
        self.model.add(Dropout(0.15))
        self.model.add(Dense(num_outputs, activation='sigmoid'))

        self.model.compile(loss=keras.losses.mean_squared_error,
                    optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])

        print('model created with # params: {}'.format(self.model.count_params()))

    def fit(self, x_train, y_train, epochs=1):
        # train
        if K.image_data_format() == 'channels_first':
            x_train = x_train.reshape(x_train.shape[0], 1, self.img_rows, self.img_cols)
        else:
            x_train = x_train.reshape(x_train.shape[0], self.img_rows, self.img_cols, 1)

        checkpointer = ModelCheckpoint(filepath='./weights-{epoch:02d}-{val_acc:.2f}.hdf5', verbose=1, save_best_only=True)
        self.model.fit(x_train, y_train, epochs=epochs, validation_split=.1, callbacks=[checkpointer])

    def predict(self, img):
        if K.image_data_format() == 'channels_first':
            img = img.reshape(1, 1, self.img_rows, self.img_cols)
        else:
            img = img.reshape(1, self.img_rows, self.img_cols, 1)

        return self.model.predict(img)[0]

    def predict_average(self, imgs):
        preds = np.zeros(18)
        for img in imgs:
            preds += self.predict(img)

        return np.round(preds/len(imgs))