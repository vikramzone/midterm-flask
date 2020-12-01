
from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.json_util import dumps
from flask_cors import CORS


#connect to database
client = MongoClient('localhost', 27017)
db = client.mydb

app = Flask(__name__) # initialize the flask app
CORS(app)


@app.route('/add_task',methods=['POST'])
def add_task():
    data=request.get_json()
    db['to-do'].insert_one(data)
    return dumps(data)

@app.route('/get_tasks')
def get_all_tasks():
    data=list(db['to-do'].find())
    return dumps(data)

@app.route('/update_task',methods=['POST'])
def update_task():
    task=request.get_json()['task']
    name=request.get_json()['name']
    myquery = {"task": task,"name":name}
    newvalues = {"$set": {'status': 'Done'}}
    db['to-do'].update_many(myquery,newvalues)
    return "successfully updated"


@app.route('/delete_task',methods=['POST'])
def delete_task():
    task=request.get_json()['task']
    name=request.get_json()['name']
    myquery = {"task": task,"name":name}
    db['to-do'].delete_many(myquery)
    return "successfully deleted"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
