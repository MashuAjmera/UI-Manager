from flask import Flask, jsonify, render_template, request, send_from_directory
from dotenv import load_dotenv
import psutil

from werkzeug import serving
import ssl, os, sys, subprocess, json

load_dotenv()  # take environment variables from .env.

HTTPS_ENABLED = True
VERIFY_USER = True

API_HOST = "0.0.0.0"
API_PORT = 5000
API_CRT = "server_cert.pem"
API_KEY = "server_key.pem"
API_CA_T = "server_cert.pem"

app = Flask(__name__,static_folder='build')

def sudo(cmd):
    pwd = '12345678'
    subprocess.run('echo {} | sudo -S {}'.format(pwd,cmd),shell=True)

@app.route('/api/getmac')
def getmac():
    x = subprocess.run('ip -j link', capture_output=True, shell=True)
    j=x.stdout.decode()
    y=json.loads(j)
    return jsonify(y[1]['address'])

@app.route('/api/getip')
def getip():
    x = subprocess.run('hostname -I', capture_output=True, shell=True)
    return jsonify(x.stdout.decode())

@app.route('/api/setmac',methods=['POST'])
def setmac():
    dname='enp0s3'
    sudo(f'ip link set dev {dname} down')
    sudo(f'ip link set dev {dname} address {request.json["mac"]}')
    sudo(f'ip link set dev {dname} up')
    return jsonify('MAC Address changed successfully!')

@app.route('/api/setip',methods=['POST'])
def setip():
    dname='enp0s3'
    sudo(f'nmcli device modify {dname} ipv4.address {request.json["ip"]}')
    return jsonify('IP Address added successfully!')

@app.route("/api/info")
def info():
    # print(psutil.virtual_memory())
    return jsonify({
        'system-version':sys.version,
        'os-name':os.name,
        'os-uname':os.uname(),
        'virtual-memory':psutil.virtual_memory(),
        'system-platform':sys.platform,
        'default-encoding':sys.getdefaultencoding(),
        #Physical cores
        "Number of physical cores": psutil.cpu_count(logical=False),
        #Logical cores
        "Number of logical cores": psutil.cpu_count(logical=True),
        #Current frequency
        "Current CPU frequency": psutil.cpu_freq().current,
        #Min frequency
        "Min CPU frequency": psutil.cpu_freq().min,
        #Max frequency
        "Max CPU frequency": psutil.cpu_freq().max,
        #System-wide CPU utilization
        "Current CPU utilization": psutil.cpu_percent(interval=1),
        #System-wide per-CPU utilization
        "Current per-CPU utilization": psutil.cpu_percent(interval=1, percpu=True),
        #Total RAM
        "Total RAM installed": round(psutil.virtual_memory().total/1000000000, 2),
        #Available RAM
        "Available RAM": round(psutil.virtual_memory().available/1000000000, 2),
        #Used RAM
        "Used RAM": round(psutil.virtual_memory().used/1000000000, 2),
        #RAM usage
        "RAM usage": psutil.virtual_memory().percent,
    })


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
            context.load_verify_locations(API_CA_T)
        try:
            context.load_cert_chain(API_CRT, API_KEY)
        except Exception as e:
            sys.exit("Error starting flask server. " + "Missing cert or key. Details: {}".format(e))
    serving.run_simple(API_HOST, API_PORT, app, ssl_context=context)