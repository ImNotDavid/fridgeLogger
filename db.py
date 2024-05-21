import sqlite3 as sq
from sqlite3 import IntegrityError
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

config = {**os.environ}

try:
    DB_PATH = config['DB_PATH']
except KeyError:
    raise Exception('No DB_PATH in env')
    

def initDB():
    conn = sq.connect(DB_PATH)
    conn.execute('''CREATE TABLE DATA 
                    (ID      INT                     NOT NULL,
                    TIMESTAMP DATETIME               NOT NULL,
                    VALUE   REAL                     NOT NULL);
                 ''')
    conn.execute('''CREATE TABLE NAMES
                    (ID     INT     PRIMARY KEY     NOT NULL,
                     NAME   TEXT                    NOT NULL);
                 ''')
    conn.close()
    
def saveTemp(temp,deviceID):
    timestamp = datetime.datetime.now()
    conn = sq.connect(DB_PATH)
    
    conn.execute('''INSERT INTO DATA (ID,TIMESTAMP,VALUE) VALUES (?,?,?)''',[deviceID,timestamp,temp])
    conn.commit()
    
    conn.close()

def createSensor(deviceID, name):
    conn = sq.connect(DB_PATH)
    try:
        conn.execute('''INSERT INTO NAMES (ID,NAME) VALUES(?,?)''',[deviceID,name])
        conn.commit()
        conn.close()
    except IntegrityError:
        print("Sensor already exists")
        conn.close()

def getTemps(deviceID):
    conn = sq.connect(DB_PATH)
    cur = conn.cursor()
    try:
        cur.execute('''SELECT * FROM DATA WHERE ID = ?''', (deviceID,))
        data = cur.fetchall()
    except:
        data = []
    return data 


