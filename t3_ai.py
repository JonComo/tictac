import numpy as np
import keras
from keras.models import Sequential
from keras.layers import Dense, Activation
from keras import backend as K
from keras.callbacks import ModelCheckpoint
from keras.models import model_from_json

class AI():
    def __init__(self, weights_path=None):
        self.create_model()
        if weights_path:
            print('loading model weights from path: {}'.format(weights_path))
            self.model.load_weights(weights_path, by_name=False)
            print('loaded weights')
    
    def create_model(self, hdim=32):
        self.model = Sequential([
            Dense(hdim, input_dim=9),
            Activation('tanh'),
            Dense(1),
            Activation('linear'),
        ])

        self.model.compile(loss=keras.losses.mean_squared_error,
                        optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])

        print('model created with # params: {}'.format(self.model.count_params()))
    
    def fit(self, x_train, y_train, epochs=1):
        # train
        checkpointer = ModelCheckpoint(filepath='./t3_weights-{epoch:02d}-{val_acc:.2f}.hdf5', verbose=1, save_best_only=True)
        self.model.fit(x_train, y_train, epochs=epochs, validation_split=.1, callbacks=[checkpointer])
        
    def best_move(self, state):
        available = np.argwhere(state==0).flatten()
        maxv = -100000
        besta = -1
        for a in available:
            # get its value
            test_state = state.copy()
            test_state[a] = 1
            value = self.model.predict(test_state.reshape(1, 9))[0,0]
            if value > maxv:
                maxv = value
                besta = a

        if besta == -1:
            print('whoops, dunno the answer')
        return besta

def winner(state):
    state = np.reshape(state, [3,3])
    ones = np.ones(3)
    
    # check horizontal wins
    h = np.dot(ones, state)
    
    if np.any(h == 3):
        return 1
    elif np.any(h == -3):
        return -1
    
    # check vertical wins
    v = np.dot(state, ones)
    
    if np.any(v == 3):
        return 1
    elif np.any(v == -3):
        return -1
    
    # check diags
    dsum = np.sum(np.diag(state))
    if dsum == 3:
        return 1
    elif dsum == -3:
        return -1
    
    dsum = np.sum(np.diag(np.flipud(state)))
    if dsum == 3:
        return 1
    elif dsum == -3:
        return -1
    
    return 0

def draw(state):
    return not np.any(state==0)

k = {0: "- ", -1: "O ", 1: "X "}
def vis(state):
    s = ""
    for i in range(9):
        if i%3 == 0:
            s += "\n"
        s += k[state[i]]
        
    print(s)