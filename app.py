#! /usr/bin/env python3
###############################################################################

from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS, cross_origin
import argparse
from pprint import pprint as pp

###############################################################################
parser = argparse.ArgumentParser(description="Simple Flask/Mongo test applition")

parser.add_argument(
    "--mongo",
    dest="mongo",
    default="mongodb://localhost:27017/flask-mongo-testdb",
    help="URI to mongodb")

args = parser.parse_args()

###############################################################################

app = Flask("TestApp")
CORS(app)

app.config["MONGO_DBNAME"] = "hellos"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/flask-mongo-testdb"
app.config["MONGO_URI"] = args.mongo

mongo = PyMongo(app)

###############################################################################
@app.route("/api/hello", methods=["GET"])
def get_hellos():

    coll = mongo.db.hello
    res = []
    for i in coll.find():
        res.append({
            "id": str(i["_id"]),
            "name": i["name"],
            "msg": i["msg"]
            })

    return jsonify({"result": res})


###############################################################################
@app.route("/api/hello", methods=["POST"])
def post_hello():

    coll = mongo.db.hello

    try:
        name = request.json["name"]
        msg = request.json["msg"]
    except KeyError:
        abort(400)

    hello_id = coll.insert({"name": name, "msg": msg})
    hello_new = coll.find_one({"_id": hello_id})
    result = {
        "name": hello_new["name"],
        "msg": hello_new["msg"]
        }
    return jsonify(result)


###############################################################################
@app.route("/api/hello/<ObjectId:hello_id>", methods=["GET"])
def get_hello(hello_id):

    coll = mongo.db.hello
    hello = coll.find_one_or_404({"_id": hello_id})
    result = {
        "name": hello["name"],
        "msg": hello["msg"]
        }
    return jsonify(result)


###############################################################################
@app.route("/api/hello/<ObjectId:hello_id>", methods=["DELETE"])
def delete_hello(hello_id):

    coll = mongo.db.hello
    result = coll.delete_one({"_id": hello_id})
    return str(result.deleted_count) + " deleted"


###############################################################################
if __name__ == "__main__":
    app.run(debug=True)
