# -*- coding:utf-8 -*-

## the function of this file is that it gets a picture(processed) of hand-written number,
## and returns the prediction from the model.

# here i use the model from [link1] below
# https://github.com/tensorflow/tensorflow/blob/r1.4/tensorflow/examples/tutorials/mnist/mnist_deep.py
# i trained the model for 20000 times and get the accuracy of 99.4%. then i saved the model to use it here.



# modules needed
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import tensorflow as tf
from PIL import Image
import matplotlib.pyplot as mt
import warnings
import time
# import datetime

FLAGS = None

# set the time data needed by cassandra table
def time_setting():
  # timeset = datetime.datetime.now()
  timeset = time.strftime('%Y-%m-%d %H:%M:%S')
  return timeset

# get pixel values and normalize them into white(0) and black(1).
def importpic(pic):
    mt.imshow(pic)
    data = list(pic.getdata())
    result = [(255-x)*1.0/255.0 for x in data]
    return result

# from [link1]
def deepnn(x):
  """deepnn builds the graph for a deep net for classifying digits.

  Args:
    x: an input tensor with the dimensions (N_examples, 784), where 784 is the
    number of pixels in a standard MNIST image.

  Returns:
    A tuple (y, keep_prob). y is a tensor of shape (N_examples, 10), with values
    equal to the logits of classifying the digit into one of 10 classes (the
    digits 0-9). keep_prob is a scalar placeholder for the probability of
    dropout.
  """
  # Reshape to use within a convolutional neural net.
  # Last dimension is for "features" - there is only one here, since images are
  # grayscale -- it would be 3 for an RGB image, 4 for RGBA, etc.
  with tf.name_scope('reshape'):
    x_image = tf.reshape(x, [-1, 28, 28, 1])

  # First convolutional layer - maps one grayscale image to 32 feature maps.
  with tf.name_scope('conv1'):
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])
    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)

  # Pooling layer - downsamples by 2X.
  with tf.name_scope('pool1'):
    h_pool1 = max_pool_2x2(h_conv1)

  # Second convolutional layer -- maps 32 feature maps to 64.
  with tf.name_scope('conv2'):
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])
    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)

  # Second pooling layer.
  with tf.name_scope('pool2'):
    h_pool2 = max_pool_2x2(h_conv2)

  # Fully connected layer 1 -- after 2 round of downsampling, our 28x28 image
  # is down to 7x7x64 feature maps -- maps this to 1024 features.
  with tf.name_scope('fc1'):
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7*7*64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

  # Dropout - controls the complexity of the model, prevents co-adaptation of
  # features.
  with tf.name_scope('dropout'):
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

  # Map the 1024 features to 10 classes, one for each digit
  with tf.name_scope('fc2'):
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.matmul(h_fc1_drop, W_fc2) + b_fc2
  return y_conv, keep_prob


def conv2d(x, W):
  """conv2d returns a 2d convolution layer with full stride."""
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
  """max_pool_2x2 downsamples a feature map by 2X."""
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')


def weight_variable(shape):
  """weight_variable generates a weight variable of a given shape."""
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def bias_variable(shape):
  """bias_variable generates a bias variable of a given shape."""
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


def get_result(pic,filename):
  # Import data
  # mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)
  result = importpic(pic)

  # Create the model
  x = tf.placeholder(tf.float32, [None, 784])

  # Define loss and optimizer
  # y_ = tf.placeholder(tf.float32, [None, 10])

  # Build the graph for the deep net
  y_conv, keep_prob = deepnn(x)

  # def the saver of the model
  saver = tf.train.Saver()

  with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    # get work dictionary path and read the model exec by [link1]
    pathhalf = os.path.dirname(__file__)
    pathwhole = os.path.join(pathhalf, 'mnist_model2.ckpt')
    saver.restore(sess,pathwhole)
    # predict the result number
    predict = tf.argmax(y_conv,1)
    predint = predict.eval(feed_dict = {x:[result],keep_prob:1.0}, session = sess)
    # print(predint)

    # print("the prediction result is : %d" %predint[0])
    predintt = str(predint[0])
    result_m = (filename,predintt,time_setting())
  return result_m

if __name__ == '__main__':
  warnings.filterwarnings('ignore')
  # test if get_result() work with local file
  # pic = Image.open('/home/cecilia/PycharmProjects/L2/flaskandmnist/saveimage/2019-08-15-19_44_26image.jpg')
  # print(get_result(pic,'test9.jpg'))
  # rst = get_result(pic,'test7.jpg')
  # print(type(rst))

