from keras.models import Model
from keras.models import load_model
from keras import applications
from keras.preprocessing.image import save_img
from keras import backend as K
import keras.layers as LAYERS
from keras.models import Sequential
from keras.layers import *
from keras.preprocessing.image import img_to_array
from keras import backend

import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import Image as pil_image

import time
import os

import numpy as np
import math

from PIL import Image
from os.path import isfile, join
from os import listdir

from joblib import Parallel, delayed