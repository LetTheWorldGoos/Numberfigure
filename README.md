# Numberfigure
## About the program

This program is about the process of inputting a hand-written number **from 0 to 9** and getting the prediction of the MNIST model on the website.

**Here is the link of the model used:*https://github.com/tensorflow/tensorflow/blob/r1.4/tensorflow/examples/tutorials/mnist/mnist_deep.py***
 
You can input the number in two ways: submitin image files or drawing a number in the given drawboard. When the output is given, the data of the upload image is sending to a certain database in cassandra container.

The whole interaction is based on python-flask and html **including js**.
 
If you want to try this program, you should complete the process in **What you need to start the program** before running the **'flask_1.py'** to get start.

Besides, if you are confused about the contents/steps of each py file in this program, you can check the comments written within. There are also comments written for the html files in the **/flaskandmnist/templates/** path.

## Functions of the program

Briefly speaking, the program offers the functions as below:

First, input the image file and save it on a website. This is realized mainly by **python-flask and basic html settlements**.

Second, draw a number image on the website and return it to a certain path. This is realized mainly by **canvas, ajax, python-flask and base64 decoding**.

Third, analyze the image and give out the prediction. This is realized by **python-Pillow and the tensorflow model**.

Fourth, set data onto the cassandra database. This is realized by **cassandra and python-cassandra-driver**.

Finally, you can pull the whole program onto the docker using the **dockerfile**.

## What you need to start the program

First, python **[Attention: version >3.0 and <3.7 is needed]** with proper modules settled. You can get the needed modules through **/flaskandmnist/requirements.txt**.

**P.S. Here, requirements.txt may give more modules than needed.**

Second, if you want the data uploaded onto the cassandra, you should get your cassandra installed. Before running the program, you should get a certain container, set its local ip and ports, create a certain keyspace and create a table in it. **You can use csd.py to help finish the last two process.**

Third, if you want to run this whole program on docker, you can use the dockerfile in the root path. It would help you to build a docker image.

Finally, since the json jquery dependency is satisfied in **/flaskandmnist/static/**, you don't have to do more for basic running of the htmls. But since canvas and ajax are used in the javascript, please make sure that your browser fits them.

That's what i want to notice about the whole program at present. Hope you could enjoy and please contact me if you have any problems or suggestions.

Thanks for your watching!
