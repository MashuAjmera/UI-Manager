from flask import Blueprint, request, jsonify
from .utils import mqtt
import json

db = Blueprint('db',__name__)

@db.route("/org",methods=['GET','POST','PUT','DELETE'])
def org():
    topic = "uimanager/influxdb"
    msg={}
    if request.method=='GET':
        msg['org']={'task':'list'}
    if request.method=='POST':
        msg['org']={
            'task':'create',
            'n':request.json['name']
        }
    elif request.method=='PUT':
        msg['org']={
            'task':'update',
            'i': request.json['id']
        }
    elif request.method=='DELETE':
        msg['org']={
            'task':'delete',
            'i':request.json['id']
        }
    return mqtt.request(json.dumps(msg),topic)


@db.route("/bucket",methods=['GET','POST','DELETE'])
def bucket():
    topic = "uimanager/influxdb"
    msg={}
    if request.method=='GET':
        msg['bucket']={'task':'list'}
    elif request.method=='POST':
        msg['bucket']={
            'task':'create',
            'n':request.json['name'],
            'o':request.json['organization'],
            'r':request.json['retentionPeriod'],
            'd':request.json['description'],
        }
    elif request.method=='DELETE':
        msg['bucket']={
            'task':'delete',
            'i':request.json['id']
        }
    return mqtt.request(json.dumps(msg),topic)

@db.route("/bucket/<which>",methods=['PUT'])
def bucketPUT(which):
    topic = "uimanager/influxdb"
    msg={}
    if(which=='retentionPeriod'):
        msg['bucket']={
            'task':'update',
            'r':request.json['retentionPeriod'],
            'i':request.json['id'],
        }
    elif(which=='name'):
        msg['bucket']={
            'task':'update',
            'n':request.json['name'],
            'o':request.json['orgID'],
            'i':request.json['id'],
        }
    return mqtt.request(json.dumps(msg),topic)


@db.route("/member",methods=['GET','POST','PUT','DELETE'])
def member():
    topic = "uimanager/influxdb"
    msg={}
    if request.method=='GET':
        msg['bucket']={
            'task':'list',
            'n':request.json['name']
        }
    if request.method=='POST':
        msg['member']={
            'task':'add',
            'n':request.json['n'],
            'm':request.json['m'],
        }
    elif request.method=='DELETE':
        msg['member']={
            'task':'remove',
            'o':request.json['o'],
            'i':request.json['i']
        }
    return mqtt.request(json.dumps(msg),topic)


@db.route("/user",methods=['GET','POST','PUT','DELETE','PATCH'])
def user():
    topic = "uimanager/influxdb"
    msg={}
    if request.method=='GET':
        msg['user']={'task':'list'}
    if request.method=='POST':
        msg['user']={
            'task':'create',
            'n':request.json['n'],
            'p':request.json['p'],
            'o':request.json['o'],
        }
    elif request.method=='DELETE':
        msg['user']={
            'task':'delete',
            'i':request.json['i']
        }
    elif request.method=='PUT':
        msg['user']={
            'task':'update',
            'i':request.json['i'],
            'n':request.json['n'],
        }
    elif request.method=='PATCH':
        msg['user']={
            'task':'password',
            'n':request.json['n'],
        }
    return mqtt.request(json.dumps(msg),topic)