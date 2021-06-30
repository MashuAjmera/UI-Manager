from flask import Flask, jsonify, request, send_from_directory, send_file
from dotenv import load_dotenv
from flask_mqtt import Mqtt

from werkzeug import serving
from werkzeug.utils import secure_filename
import ssl, os, sys, subprocess, json, time
load_dotenv()  # take environment variables from .env.

app = Flask(__name__,static_folder='build')
# from api.mqtt import mqtt
# app.register_blueprint(mqtt,url_prefix='/api/mqtt')
from api.network import network
app.register_blueprint(network,url_prefix='/api/network')

app.config['MQTT_BROKER_URL'] = '0.0.0.0'
app.config['MQTT_BROKER_PORT'] = 1883
# app.config['MQTT_USERNAME'] = 'user'
# app.config['MQTT_PASSWORD'] = 'secret'
app.config['MQTT_REFRESH_TIME'] = 1.0  # refresh time in seconds
mqtt = Mqtt(app)

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('uimanager/influxdb')

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print(f'message received {message.topic}')

@app.route("/api/publish")
def handle_publish():
    topic="uimanager/influxdb"
    result = mqtt.publish(topic, "message")
    status = result[0]
    if status == 0:
        return f"Sending to {topic} successful."
    else:
        return f"Failed to send message to topic {topic}."

HTTPS_ENABLED = True
VERIFY_USER = True
API_HOST = "0.0.0.0"
API_PORT = 5000

@app.route("/api/info")
def info():
    # print(psutil.virtual_memory())
    return jsonify({
        'system-version':sys.version,
        'os-name':os.name,
        'os-uname':os.uname(),
        'system-platform':sys.platform,
        'default-encoding':sys.getdefaultencoding(),
    })

@app.route("/api/uploader" , methods=['POST'])
def uploader():
    f = request.files['file']
    f.save(os.path.join(os.environ.get("API_UPLOAD_FOLDER"), secure_filename(f.filename)))
    return "Uploaded successfully!"

@app.route("/api/downloader")
def downloader():
    return send_file(os.path.join(os.environ.get("API_DOWNLOAD_FOLDER"), 'alice.p12'),as_attachment=True)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if os.environ.get("FLASK_ENV")!='development':
        if path != "" and os.path.exists(app.static_folder + '/' + path):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    context = None
    if HTTPS_ENABLED and os.environ.get("FLASK_ENV")!='development':
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        if VERIFY_USER:
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(os.environ.get("API_CA_T"))
        try:
            context.load_cert_chain(os.environ.get("API_CRT"), os.environ.get("API_KEY"))
        except Exception as e:
            sys.exit("Error starting flask server. " + "Missing cert or key. Details: {}".format(e))
    serving.run_simple(API_HOST, API_PORT, app, ssl_context=context)