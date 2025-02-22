import logging
import numpy as np
import keras
from utils.data_prep_utils import load_h5_files
from utils.pointclouds_utils import pc_batch_preprocess
from utils.pointclouds_utils import eigen_tree_index_2
from scipy.spatial import cKDTree
from multiprocessing import Pool
import h5py
import os

def kdtree_index(X):
    nb = X.shape[0]
    for i in range(nb):
        x = X[i, ...]
        T = cKDTree(x)
        X[i, ...] = np.take(x, T.indices, axis=0)
    return X

def eigen_tree_index_2_(X):
    nb = X.shape[0]
    for i in range(nb):
        x = X[i, ...]
        X[i, ...] = eigen_tree_index_2(x, depth=4)
    return X

def tile(x, rep=16):
    return np.tile(x, (16, 1))

def index_points(X, nv):
    ns = X.shape[0]
    X_nv = X.shape[1]
    X_new = np.zeros(shape=(ns, 16*nv, 3), dtype=np.float32)
    for i in range(ns):
        x = X[i, ...]
        # x = np.expand_dims(x, axis=0)
        idx = np.random.permutation(np.arange(X_nv))[:nv]
        x = x[idx, :]
        # x = kdtree_index(x)
        x = eigen_tree_index_2(x, 4)
        # x = np.tile(x, (16, 1))
        X_new[i, ...] = x
    return X_new


class ClassificationProvider(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, files_list, data_path, n_classes, n_points,
                 batch_size=32, preprocess=list(), shuffle=True, classes=list()):
        'Initialization'
        logging.info("Loading data from %s listed in file %s", data_path, files_list)
        self.data, self.labels = load_h5_files(data_path, files_list)
        self.labels = np.reshape(self.labels, (-1,))
        self.n_points_data = np.shape(self.data)[1]
        self.n_samples = self.data.shape[0]
        self.nv = self.data.shape[1]
        self.classes = classes
        self.n_points = n_points
        # self.data = index_points(self.data, self.n_points)
        self.batch_size = batch_size
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.preprocess = preprocess
        # self.pool = Pool(4)
        self.on_epoch_end()


    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(self.n_samples / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Generate data
        X, y = self.__data_generation(indexes)
        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(self.n_samples)
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, indexes):

        idx = np.random.permutation(np.arange(self.n_points_data))[:self.n_points]
        X = self.data[indexes, ...]
        X = X[:, idx, ...]
        y = self.labels[indexes, ...]

        for i in range(len(self.preprocess)):
            X, y = pc_batch_preprocess(x=X, y=y, proc=self.preprocess[i])

        y = keras.utils.to_categorical(y, num_classes=self.n_classes)
        # y = np.expand_dims(y, axis=1)
        # y = np.repeat(y, axis=1, repeats=12)
        # print('y shape !! ', y.shape)
        return X, y

    def set_preprocessing(self, preprocessing):
        self.preprocess = preprocessing

    def get_data(self):
        return self.data, self.labels

def load_h5_data_multires_(h5_filename, num_points):
    f = h5py.File(h5_filename)
    data = f['data'][:]
    sub_idx = []
    for i in range(len(num_points)):
        sub_idx.append(f['sub_idx_' + str(num_points[i])])

    class_label = f['class_label'][:]

    if 'part_label' in f:
        part_label = f['part_label'][:]
        return (data, sub_idx, part_label, class_label)
    else:
        return (data, sub_idx, class_label)

def load_h5_data_multires(data_path, files_list_path, num_points):
    files_list = [line.rstrip() for line in open(files_list_path)]
    data = []
    labels = []
    sub_idx = []
    for j in range(len(num_points)):
        sub_idx.append([])
    for i in range(len(files_list)):
        data_, sub_idx_, labels_ = load_h5_data_multires_(os.path.join(data_path, files_list[i]), num_points)
        data.append(data_)
        for j in range(len(sub_idx_)):
            sub_idx[j].append(sub_idx_[j])
        labels.append(labels_)
    data = np.concatenate(data, axis=0)
    for j in range(len(num_points)):
        sub_idx[j] = np.concatenate(sub_idx[j], axis=0)
    labels = np.concatenate(labels, axis=0)
    return data, sub_idx, labels


class ClassificationProvider2(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, files_list, data_path, n_classes, n_points,
                 batch_size=32, preprocess=list(), shuffle=True, classes=list()):
        'Initialization'
        # self.data, self.labels = load_h5_files(data_path, files_list)
        self.data, self.sub_idx, self.labels = load_h5_data_multires(data_path, files_list, n_points)

        # for j in range()

        self.labels = np.reshape(self.labels, (-1,))
        self.n_points_data = np.shape(self.data)[1]
        self.n_samples = self.data.shape[0]
        self.nv = self.data.shape[1]
        self.classes = classes
        self.n_points = n_points
        # self.data = index_points(self.data, self.n_points)
        self.batch_size = batch_size
        self.n_classes = n_classes
        self.shuffle = shuffle
        self.preprocess = preprocess
        # self.pool = Pool(4)
        self.X = []
        for j in range(len(n_points)):
            self.X.append(np.zeros((batch_size, n_points[j], 3)))
        self.on_epoch_end()


    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(self.n_samples / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Generate data
        X, y = self.__data_generation(indexes)
        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(self.n_samples)
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, indexes):

        x = self.data[indexes, ...]

        for j in range(len(self.n_points)):
            sub_idx = self.sub_idx[j][indexes, ...]
            for k in range(x.shape[0]):
                idx = sub_idx[k, ...]
                self.X[j][k, ...] = x[k, idx, ...]



        # idx = np.random.permutation(np.arange(self.n_points_data))[:self.n_points]
        # X = self.data[indexes, ...]
        # X = X[:, idx, ...]
        y = self.labels[indexes, ...]

        """
        for i in range(len(self.preprocess)):
            X, y = pc_batch_preprocess(x=X, y=y, proc=self.preprocess[i])
        """

        y = keras.utils.to_categorical(y, num_classes=self.n_classes)
        # y = np.expand_dims(y, axis=1)
        # y = np.repeat(y, axis=1, repeats=12)
        # print('y shape !! ', y.shape)
        return self.X, y

    def set_preprocessing(self, preprocessing):
        self.preprocess = preprocessing

    def get_data(self):
        return self.data, self.labels