from flask import Blueprint, request, jsonify
from .utils import mqtt
import json

db = Blueprint('db',__name__)

@db.route("/retention",methods=['GET'])
def retention():
    thisdict = {
        "retention": request.args['days']
    }
    topic = "uimanager/influxdb"
    msg = json.dumps(thisdict)
    result=mqtt.publish(msg,topic) 
    status = result[0]
    if status == 0:
        return f"Send `{msg}` to topic `{topic}`"
    else:
        return f"Failed to send message to topic {topic}"

@db.route("/bucket/<name>",methods=['GET'])
def bucket(name):
    thisdict = {
        "bucket": name
    }
    topic = "uimanager/influxdb"
    msg = json.dumps(thisdict)
    result=mqtt.publish(msg,topic) 
    status = result[0]
    if status == 0:
        return f"Send `{msg}` to topic `{topic}`"
    else:
        return f"Failed to send message to topic {topic}"