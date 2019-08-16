# -*- coding:utf-8 -*-

## this file is to handle with the form changes.
## In the 1.5 part of flask_1, we have to change the image from base64 form to PIL binarized image in 28*28px.
## this file is responsible for such process.

# modules needed
from PIL import Image
import warnings
import time
import os
import io
import base64

# this function is to change the base64 file to image
def base64toImage(file_in):
    # the b64decode() function asks '==' as its endding, but the return value from json doesn't give it.
    # if your return value from json does have such endding, you can pass this line
    # (you can check the base64 code by uncommenting line76 in flask_1)
    file_in = file_in.split(",")[1] + "==" #
    file_in = base64.b64decode(file_in)
    # into PIL image
    file_in = io.BytesIO(file_in)
    image = Image.open(file_in)
    return image


# this function is to change the size of image into 28*28px, and then make the binarization.
def produceImage(txt):
    image = base64toImage(txt)
    # change the size to 28*28
    resized_image = image.resize((28, 28), Image.ANTIALIAS)
    #  get gray-scale image first
    image2 = resized_image.convert('L')
    # Binatization part
    table = []
    for i in range(256):
        if i < 100:
            table.append(0)
        else:
            table.append(1)
    image2 = image2.point(table,'1')

    # save the processed image by a relative path
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    file_outname = now + r"image.jpg"
    path0 = os.path.dirname(__file__)
    path1 = os.path.join(path0, 'saveimage', file_outname)
    image2.save(path1)
    # here path1 is the path for MNIST_r to read the image, fileoutname is the name of the image
    outputimage = (path1, file_outname)
    return outputimage

if __name__ == '__main__':
    warnings.filterwarnings('ignore')

    # here i give a base64 image as example
    # test = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAcABwBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/APf64uf4seCrbWZdHfV5DqEdwbVreOyuHYyhtuwbUO47uOM57V2lFFcf4QtpdD1zxHo10uGuNQl1Wzm8pIxPDNgsBg5do3yrFuQGj6BlA7CiiubtvD99P4xk13Wbq0uEs0kg0mCG32+Qkm0vI5YkmU7QmVIG1ScDeQOkooooor//2Q"
    # produceImage(test)
    # test: watch the elements in the ouput
    # x = produceImage(test)
    # print(x)