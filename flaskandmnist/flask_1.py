# -*- coding:utf-8 -*-

## this file is the engine of the whole program, please start this file, then open the ip appeared in console.

## 0. modules needed
# 0.1 use absolute path and use accurate '/'
from __future__ import absolute_import
from __future__ import division

# 0.2 to get work dictionary
import os

# 0.3 get flask and get decode package
from flask import Flask, render_template, request,jsonify, abort
from urllib.parse import unquote
from PIL import Image

# 0.4 connect with other py files
import MNIST_r
import csd
import transfile


## 1. setting flask websites

# 1.1 set app
app = Flask(__name__)


# 1.2 set index page
@app.route('/')
def getpic():
    return render_template('index.html')

# 1.3 set answer page no.1
# by submitting required pictures from index.html, we get answer using the following function
@app.route('/upload', methods = ['GET','POST'])
def processpic():
    if request.method == 'POST':
        # get image with filestorage form
        pic = request.files['file']
        # get name of the input image
        picname = pic.filename
        # save the image in wd path
        path0 = os.path.dirname(__file__)
        path1 = os.path.join(path0,'saveimage',picname)
        pic.save(path1)
        # analyze the image with tensorflow model
        pic1 = Image.open(path1)
        target = MNIST_r.get_result(pic1,picname)
        #  send the message to another docker container
        csd.insertnewinfo(target)
    else:
        target = None
    return render_template('output.html',target = target[1])

# 1.4 set drawboard page
# by clicking the shift link we could get here.
# use json script to create the drawboard and use ajax to return data to '/upload3'
@app.route('/upload2', methods = ['GET','POST'])
def movetojs():
    return render_template('jsonpic2.html')

# 1.5 set processing page
# since the canvas drawboard returns a json file with base64 code,
# here we split the target code and decode it,
# then we use the similar process as that in 1.3
@app.route('/upload3', methods=['POST'])  # only post allowed 'GET',
def jsonpic():
    if request.method == 'POST':
        # get the data from ajax
        data = request.get_data().decode('utf-8')
        data = unquote(data)
        # transform data into PIL image
        img_base64 = data.split('=')[1]
        # print(img_base64)
        datapic = transfile.produceImage(img_base64)
        pic2 = Image.open(datapic[0])
        picname2 = datapic[1]
        target2 = MNIST_r.get_result(pic2,picname2)
        csd.insertnewinfo(target2)
        return jsonify(status='success', data=target2[1])
        # here data is sent back to ajax; and ajax saves the data while getting to the 'result' page

# 1.6 set answer page no.2
@app.route('/result', methods=['GET'])
def result():
    data = request.args.get('data')  # use GET to receive the data
    if not data:
        abort("error!")
    return render_template('output.html', target=data)



if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0', port=5000)
