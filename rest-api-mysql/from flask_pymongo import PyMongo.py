from flask_pymongo import PyMongo
import flask
from flask import Flask, request
import json
import os
app = flask.Flask(__name__)

#mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/todo_db")
#db = mongodb_client.db

app.config["MONGO_URI"] = "mongodb://localhost:27017/thuchanh"
mongodb_client = PyMongo(app)
db = mongodb_client.db

@app.route("/add_one", methods=['POST'])
def add_one():
    jsondata = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        jsondata = request.data
        jsondata = json.loads(jsondata)
        print ('data load: ' + str(jsondata))
    if jsondata !=None:
        try:
            print("data add new: ", jsondata)
            db.todos.insert_one(jsondata)
        except BulkWriteError as e:
            return flask.jsonify(message="duplicates encountered and ignored",
                             details=e.details,
                             inserted=e.details['nInserted'],
                             duplicates=[x['op'] for x in e.details['writeErrors']])
    return flask.jsonify(message="success"), 201

from pymongo.errors import BulkWriteError

@app.route("/add_many")
def add_many():
    try:
        todo_many = db.todos.insert_many([
            {'_id': 1, 'title': "todo title one ", 'body': "todo body one "},
            {'_id': 8, 'title': "todo title two", 'body': "todo body two"},
            {'_id': 2, 'title': "todo title three", 'body': "todo body three"},
            {'_id': 9, 'title': "todo title four", 'body': "todo body four"},
            {'_id': 10, 'title': "todo title five", 'body': "todo body five"},
            {'_id': 5, 'title': "todo title six", 'body': "todo body six"},
        ], ordered=False)
    except BulkWriteError as e:
        return flask.jsonify(message="duplicates encountered and ignored",
                             details=e.details,
                             inserted=e.details['nInserted'],
                             duplicates=[x['op'] for x in e.details['writeErrors']])

    return flask.jsonify(message="success", insertedIds=todo_many.inserted_ids)

@app.route("/")
def home():
    try:
        todos = db.todos.find({"_id": 1})
        return flask.jsonify([todo for todo in todos])
    except:
        return "home page"
@app.route("/get_todo/<int:todoId>",methods=['GET'])
def get_todo(todoId):
    try:
        todo = db.todos.find_one({"_id": todoId})
        return todo
    except:
        print("error")
        return None
@app.route("/replace_todo/<int:todoId>")
def replace_one(todoId):
    result = db.todos.replace_one({'_id': todoId}, {'title': "modified title"})
    return {'id': result.raw_result}

@app.route("/update_todo/<int:todoId>")
def update_one(todoId):
    result = db.todos.update_one({'_id': todoId}, {"$set": {'title': "updated title"}})
    return result.raw_result

@app.route("/delete_todo/<int:todoId>", methods=['DELETE'])
def delete_todo(todoId):
    todo = db.todos.find_one_and_delete({'_id': todoId})
    if todo is not None:
        return todo.raw_result
    return "ID does not exist"
if __name__ == '__main__':

    homeDir = os.environ['HOME']
    port = homeDir.split("/")[-1][2:7]

    print("Personal API Port: %s" %(port))

    app.run(port=int(6789),host='0.0.0.0',use_reloader=False)