import sys
sys.path.append('..')
from utils import *

import argparse
from keras.models import *
from keras.layers import *
from keras.optimizers import *

"""
NeuralNet for the game of TicTacToe.

Author: Evgeny Tyurin, github.com/evg-tyurin
Date: Jan 5, 2018.

Based on the OthelloNNet by SourKream and Surag Nair.
"""
class TicTacToeNNet():
    def __init__(self, game, args):
        # game params
        self.board_x, self.board_y = game.getBoardSize()
        self.action_size = game.getActionSize()
        self.args = args

        # Neural Net
        self.input_boards = Input(shape=(self.board_x, self.board_y))    # s: batch_size x board_x x board_y

        x_image = Reshape((self.board_x, self.board_y, 1))(self.input_boards)                # batch_size  x board_x x board_y x 1
        h_conv1 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels_1, 3, strides=3, padding='valid')(x_image)))
        h_conv2 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels_2, 1, strides=1, padding='valid')(h_conv1)))         # batch_size  x board_x x board_y x num_channels
        h_conv3 = Activation('relu')(BatchNormalization(axis=3)(Conv2D(args.num_channels_3, 1, strides=1, padding='valid')(h_conv2)))         # batch_size  x board_x x board_y x num_channels
        h_conv3_flat = Flatten()(h_conv3)
        s_fc1 = Dropout(args.dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(args.dense_1)(h_conv3_flat))))  # batch_size x 1024
        s_fc2 = Dropout(args.dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(args.dense_2)(s_fc1))))          # batch_size x 1024
        s_fc3 = Dropout(args.dropout)(Activation('relu')(BatchNormalization(axis=1)(Dense(args.dense_3)(s_fc2))))          # batch_size x 1024
        self.pi = Dense(self.action_size, activation='softmax', name='pi')(s_fc2)   # batch_size x self.action_size
        self.v = Dense(1, activation='tanh', name='v')(s_fc3)                    # batch_size x 1

        self.model = Model(inputs=self.input_boards, outputs=[self.pi, self.v])
        self.model.compile(loss=['categorical_crossentropy','mean_squared_error'], optimizer=Adam(args.lr))
        #print(self.model.summary())
