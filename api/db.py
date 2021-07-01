from flask import Blueprint, request, jsonify
from .utils import mqtt
import json

db = Blueprint('db',__name__)

@db.route("/retention",methods=['GET','POST','PUT','DELETE'])
def retention():
    topic = "uimanager/influxdb/retention"
    if request.method=='POST':
        msg={
            'TASK':'CREATE',
            'POLICY':request.json['POLICY'],
            'ON':request.json['ON'],
            'DURATION':request.json['DURATION'],
            'REPLICATION':request.json['REPLICATION'],
            'SHARD':request.json['SHARD'],
            'DEFAULT':request.json['DEFAULT']
        }
        return mqtt.publish(json.dumps(msg),topic)
    elif request.method=='PUT':
        msg={
            'TASK':'ALTER',
            'POLICY':request.json['POLICY'],
            'ON':request.json['ON'],
            'DURATION':request.json['DURATION'],
            'REPLICATION':request.json['REPLICATION'],
            'SHARD':request.json['SHARD'],
            'DEFAULT':request.json['DEFAULT']
        }
        return mqtt.publish(json.dumps(msg),topic)
    elif request.method=='DELETE':
        msg={
            'TASK':'DROP',
            'POLICY':request.json['POLICY'],
            'ON':request.json['ON']
        }
        return mqtt.publish(json.dumps(msg),topic)


@db.route("/organization",methods=['GET','POST','PUT','DELETE'])
def organization():
    topic = "uimanager/influxdb/organization"
    if request.method=='POST':
        msg={
            'TASK':'CREATE',
            'n':request.json['n']
        }
        return mqtt.publish(json.dumps(msg),topic)
    elif request.method=='PUT':
        msg={
            'TASK':'UPDATE',
            'i': request.json['i'],
            'n': request.json['n']
        }
        return mqtt.publish(json.dumps(msg),topic)
    elif request.method=='DELETE':
        msg={
            'TASK':'CREATE',
            'i':request.json['i']
        }
        return mqtt.publish(json.dumps(msg),topic)


@db.route("/bucket",methods=['GET','POST','PUT','DELETE'])
def bucket():
    topic = "uimanager/influxdb/bucket"
    if request.method=='POST':
        msg={
            'TASK':'CREATE',
            'n':request.json['n'],
            'o':request.json['o'],
            'r':request.json['r'],
        }
        return mqtt.publish(json.dumps(msg),topic)
    elif request.method=='PUT':
        msg={
            'TASK':'UPDATE',
            'n':request.json['n'],
            'o':request.json['o'],
            'r':request.json['r'],
            'i':request.json['i'],
        }
        return mqtt.publish(json.dumps(msg),topic)
    elif request.method=='DELETE':
        msg={
            'TASK':'CREATE',
            'n':request.json['n'],
            'o':request.json['o'],
            'i':request.json['i']
        }
        return mqtt.publish(json.dumps(msg),topic)

@db.route("/member",methods=['GET','POST','PUT','DELETE'])
def member():
    topic = "uimanager/influxdb/member"
    if request.method=='POST':
        msg={
            'TASK':'add',
            'n':request.json['n'],
            'm':request.json['m'],
        }
        return mqtt.publish(json.dumps(msg),topic)
    elif request.method=='DELETE':
        msg={
            'TASK':'remove',
            'o':request.json['o'],
            'i':request.json['i']
        }
        return mqtt.publish(json.dumps(msg),topic)

@db.route("/buckets/<name>",methods=['GET'])
def buckets(name):
    thisdict = {
        "bucket": name
    }
    topic = "uimanager/influxdb"