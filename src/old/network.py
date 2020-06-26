from keras.models import Input, Model
from keras.layers import Dense
import time
import numpy as np
"""
this constructs a deep belief network (DBN) composed of fully connected autoencoders
this model is responsible for learning the 'features' in a chess position
the input is a 772-bit one-hot encoded representation of a position
"""
def build_belief_network():
    # 1st layer: 741-500-741
    input_board = Input(shape=(772,))
    layer1 = Dense(500, activation='relu')(input_board)
    layer1 = Dense(772, activation='relu')(layer1)

    # 2nd layer: 500-300-500
    layer2 = Dense(500, activation='relu')(layer1)
    layer2 = Dense(300, activation='relu')(layer2)
    layer2 = Dense(500, activation='relu')(layer2)

    # 3nd layer: 300-200-300
    layer3 = Dense(300, activation='relu')(layer2)
    layer3 = Dense(200, activation='relu')(layer3)
    layer3 = Dense(300, activation='relu')(layer3)

    # 4nd layer: 200-100-200
    layer4 = Dense(200, activation='relu')(layer3)
    layer4 = Dense(100, activation='relu')(layer4)
    layer4 = Dense(200, activation='relu')(layer4)

    # output layer: 100
    encoded = Dense(100, activation='sigmoid')(layer4)

    model = Model(input_board, encoded)
    model.compile(optimizer='adam', loss='binary_crossentropy')

    return model


"""
this constructs a fully connected NN that judges the quality of a position and winning chances
takes inputs from a DBN
"""
def build_judgement_network():
    # 1st layer: 100 features from DBN
    input = Input(shape=(100,))
    layer1 = Dense(400, activation='relu')(input)
    layer2 = Dense(200, activation='relu')(layer1)
    layer3 = Dense(100, activation='relu')(layer2)

    # output layer: 100
    output = Dense(1, activation='sigmoid')(layer3)

    model = Model(input, output)
    model.compile(optimizer='adam', loss='binary_crossentropy')

    return model


"""
this constructs a composite model, composed of a belief network connected to a NN.
the deep belief network analyzes a position and extracts features
the NN analyze the extracted features and judge their winning chances
"""
def build_composite_model(dbn, nn):
    input = Input(shape=(772,))

    dbn_output = dbn(input)
    nn_output = nn(dbn_output)

    model = Model(input, nn_output)
    model.compile(optimizer='adam', loss='binary_crossentropy')

    return model


"""
builds and returns a composite model
"""
def factory():
    dbn = build_belief_network()
    nn = build_judgement_network()

    return dbn, nn

a, b = factory()
m = build_composite_model(a, b)
s = time.time()
m.predict(np.random.randint(0, 1, (1, 772)))
print(time.time()-s)
