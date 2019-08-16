# -*- coding:utf-8 -*-

## this file is to send information onto a certain cassandra container in docker
## in the program, the keyspace and the table is created. if you want to repeat the whole process,
## please uncomment the createKeySpace() function and use it with your own container(by setting the ip and port)

# modules needed( comment one for createKeySpace() )
import logging
from cassandra.cluster import Cluster
# from cassandra.query import SimpleStatement
# from cassandra import ConsistencyLevel


# get logs of the process
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

## the name of the target keyspace
KEYSPACE = "uploadinfo2"

## use createKeySpace after creating a cassandra container for connection

# def createKeySpace():
#     cluster = Cluster(contact_points=['0.0.0.0'], port=9042)  # local ip and port
#     session = cluster.connect()  #connect python and cassandra
#
#
#     log.info("Creating keyspace...")
#     try:
#         # create keyspace
#         session.execute("""
#         CREATE KEYSPACE %s
#         WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
#         """ %KEYSPACE)
#         # set keyspace
#         log.info("setting keyspace...")
#         session.set_keyspace(KEYSPACE)
#         # create table
#         log.info("creating table...")
#         # here the 'info1' as below is the name of the target table, if needed, change its name.
#         session.execute("""
#             CREATE TABLE info1 (
#                 updatetime text,
#                 filename text,
#                 output text,
#                 PRIMARY KEY (updatetime, filename)
#             )
#
#             """)
#     except Exception as e:
#         log.error("Unable to create keyspace")
#         log.error(e)


# insert the info from flask_1 to the target table
def insertnewinfo(target):
    cluster = Cluster(contact_points=['127.0.0.1'], port=9042)  # set ip and port
    session = cluster.connect()  # connection

    try:
        log.info("setting keyspace...")
        session.set_keyspace(KEYSPACE)
        log.info("inserting into table...")
        session.execute(
            # here the 'info1' as below is the name of the target table, if needed, change its name.
            """
                INSERT INTO info1(updatetime, filename, output)
                VALUES(%s, %s, %s)
            """,
            (target[2], target[0], target[1])
        )
    except Exception as e:
        log.error("Unable to upload, please check the code.")
        log.error(e)


# for testing
# target = ('test5.jpg', '5', '2019-08-09 11:56:50')
# createKeySpace();