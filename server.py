from flask import Flask, jsonify, render_template, request, send_from_directory, send_file
from dotenv import load_dotenv

from werkzeug import serving
from werkzeug.utils import secure_filename
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
    x = subprocess.run('hostname -i', capture_output=True, shell=True)
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
        'system-platform':sys.platform,
        'default-encoding':sys.getdefaultencoding(),
    })

@app.route("/api/uploader" , methods=['POST'])
def uploader():
    f = request.files['file']
    f.save(os.path.join(os.environ.get("FLASK_UPLOAD_FOLDER"), secure_filename(f.filename)))
    return "Uploaded successfully!"

@app.route("/api/downloader")
def downloader():
    return send_file('/home/mashu/ABB/alice.p12',as_attachment=True)

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