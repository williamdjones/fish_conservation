import os

import numpy as np

from scipy.ndimage import imread

from scipy.misc import imresize


import matplotlib.pyplot as plt

from skimage import feature
from skimage.color import rgb2grey



def load_from_folder(path,folder,batch_size):

    '''

        This function reads a bounded number of images from a particular folder. Returns a numpy array of pixel data and a numpy of labels.

    :param path:
    :param folder:
    :param batch_size:
    :return:
    '''

    path = path + '/' + folder
    label_dict = {'ALB': 0, 'BET': 1, 'DOL': 2, 'LAG': 3, 'NoF': 4, 'OTHER': 5, 'SHARK': 6, 'YFT': 7}

    l = label_dict[folder]

    filenames = []

    num_examples = 0


    filenames = os.listdir(path)


    fish_labels = l*(np.ones([batch_size, 1]))
    fish_data = np.zeros([batch_size, 600, 600,1])
    j = 0



    for file in filenames:
        # now read the images and store the labels

        if j < batch_size:
            relpath = path + '/' + file
            image = imread(relpath)

            image = imresize(image,[600,600])

            image = rgb2grey(image)

            fish_data[j,:,:,0] = image

            j = j + 1
        else:
            return fish_data, fish_labels

    return fish_data, fish_labels



def load_batch(max_ex_per_cat):
    '''
        This function iterates over each folder and pulls a number of samples (max_ex_per_cat, or maximum examples per category),
        from each category in order to form a training batch.

    '''

    batch_data = np.zeros([0,600,600,1])
    batch_labels = np.zeros([0,1])

    dirs = ['ALB','BET','DOL','LAG','NoF','OTHER','SHARK','YFT']

    for d in dirs:
        x,y = load_from_folder('train',d,max_ex_per_cat)
        batch_data = np.append(batch_data,x, axis=0)
        batch_labels = np.append(batch_labels,y,axis=0)
    return batch_data, batch_labels


def to_categorical(x,num_classes):
    cat_labels=np.zeros([x.shape[0],num_classes])

    # for each example
    for i in range(0,x.shape[0]):
        # j should be the value of the label, check this with the value of x[i]
        val = x[i]
        cat_labels[i,int(val)] = 1

    return cat_labels


def compute_canny(data, sigma):
    for i in range(0,data.shape[0]):
        data[i,:,:,0] = feature.canny(data[i,:,:,0],sigma=sigma)

    return data