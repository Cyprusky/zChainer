# coding: utf-8

import numpy as np
from chainer import Variable, ChainList, serializers
import chainer.functions as F
import chainer.links as L
import os.path
import pickle
from manager import NNManager
import utility

class NNAutoEncoder ():
    def __init__(self, encoder, decoder, optimizer,
        epoch=20, batch_size=100, log_path="", export_path=""):
        self.encoder = encoder
        self.decoder = decoder
        self.optimizer = optimizer
        self.epoch = epoch
        self.batch_size = batch_size
        self.log_path = log_path
        self.export_path = export_path
        self.autoencoded = ChainList()

    def fit(self, x_train):
        for layer in range(0, len(self.encoder)):
            # Creating model
            NNManager.forward = forward
            model = ChainList(self.encoder[layer].copy(), self.decoder[layer].copy())
            nn = NNManager(model, self.optimizer, F.mean_squared_error,
                self.epoch, self.batch_size, self.log_path)

            # Training
            x_data = self.encode(x_train, layer).data
            nn.fit(x_data, x_data, autoencoding=True)
            self.autoencoded.add_link(nn.model[0].copy())

        if self.export_path != "":
            pickle.dump(self.autoencoded, open(self.export_path, 'wb'), -1)
        return self

    def predict(self, x_test):
        raise Exception("Prediction for AutoEncoder is not implemented.")

    def encode(self, x, n):
        if n == 0:
            return Variable(x)
        else:
            h = self.encode(x, n-1)
            return F.relu(self.autoencoded[n-1](h))

def forward(self, x):
    h = F.dropout(F.relu(self.model[0](x)))
    return F.dropout(F.relu(self.model[1](h)))