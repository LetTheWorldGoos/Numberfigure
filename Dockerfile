# basic image of python
FROM python:3.6

# add content to docker use following path
ADD ./whole/flaskandmnist

# set wd
WORKDIR /flaskandmnist

# set requirements.txt
RUN pip install -r requirements.txt

CMD ["python","/flaskandmnist/flask_1.py"]
