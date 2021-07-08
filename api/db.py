from flask import Blueprint, request, jsonify
from .utils import mqtt
import json

db = Blueprint('db',__name__)

@db.route("/organization",methods=['GET','POST','PUT','DELETE'])
def organization():
    topic = "uimanager/influxdb"
    msg={}
    if request.method=='GET':
        msg['org']={'task':'list'}
    if request.method=='POST':
        msg['org']={
            'task':'create',
            'n':request.json['n']
        }
    elif request.method=='PUT':
        msg['org']={
            'task':'update',
            'i': request.json['i'],
            'n': request.json['n']
        }
    elif request.method=='DELETE':
        msg['org']={
            'task':'create',
            'i':request.json['i']
        }
    return mqtt.request(json.dumps(msg),topic)


@db.route("/bucket",methods=['GET','POST','PUT','DELETE'])
def bucket():
    topic = "uimanager/influxdb"
    msg={}
    if request.method=='GET':
        msg['bucket']={'task':'list'}
    if request.method=='POST':
        msg['bucket']={
            'task':'create',
            'n':request.json['name'],
            'o':request.json['organization'],
            'r':request.json['retentionPeriod'],
        }
    elif request.method=='PUT':
        msg['bucket']={
            'task':'update',
            'n':request.json['n'],
            'o':request.json['o'],
            'r':request.json['r'],
            'i':request.json['i'],
        }
    elif request.method=='DELETE':
        msg['bucket']={
            'task':'create',
            'n':request.json['n'],
            'o':request.json['o'],
            'i':request.json['i']
        }
    return mqtt.request(json.dumps(msg),topic)

@db.route("/member",methods=['GET','POST','PUT','DELETE'])
def member():
    topic = "uimanager/influxdb"
    msg={}
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

@db.route("/buckets/<name>",methods=['GET'])
def buckets(name):
    msg = {}
    msg['org']={"task":'create','n':'abb'}
    msg['bucket']={"task":'create','n':'bucket1','o':'abb','r':'72h'}
    topic = "uimanager/influxdb"
    return jsonify(mqtt.request(json.dumps(msg),topic))