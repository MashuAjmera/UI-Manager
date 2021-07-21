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
            'n':request.json['name'],
            'd':request.json['description']
        }
    elif request.method=='PUT':
        msg['org']={
            'task':'update',
            'i': request.json['id']
        }
        if 'name' in request.json.keys():
            msg['org']['name']=request.json['name']
        elif 'description' in request.json.keys():
            msg['org']['description']=request.json['description']
    elif request.method=='DELETE':
        msg['org']={
            'task':'delete',
            'i':request.json['id']
        }
    return mqtt.request(json.dumps(msg),topic)

@db.route("/bucket",methods=['GET','POST','DELETE', 'PUT'])
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
    elif request.method=='PUT':
        msg['bucket']={
            'task':'update',
            'i': request.json['id']
        }
        if 'name' in request.json.keys():
            msg['bucket']['n']=request.json['name']
        elif 'description' in request.json.keys():
            msg['bucket']['d']=request.json['description']
        elif 'retentionPeriod' in request.json.keys():
            msg['bucket']['r']=request.json['retentionPeriod']
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

@db.route("/query",methods=['GET'])
def query():
    topic = "uimanager/influxdb"
    msg={}
    if request.method=='GET':
        msg['query']={
            'start':'-35d6h'
        }
    return mqtt.request(json.dumps(msg),topic)

@db.route("/write",methods=['GET'])
def write():
    topic = "uimanager/influxdb"
    msg={}
    if request.method=='GET':
        msg['write']={
            "message" : 
            {
                "data" : 
                {
                    "paramId" : "01_01",
                    "status" : 
                    {
                        "code" : False,
                        "message" : "",
                        "value" : 267,
                        "valueType" : "int32"
                    },
                    "timestamp" : "2021-06-15T13:55:29.994Z",
                    "unit" : "kW",
                    "value" : 
                    {
                        "value" : 267,
                        "valueType" : "int32"
                    }
                },
                "serial" : "drivesim-065b6d62-2"
            },
            "messageId" : 29737547,
            "requestId" : 0,
            "type" : "MONITORING_DATA"
        }
    return mqtt.request(json.dumps(msg),topic)