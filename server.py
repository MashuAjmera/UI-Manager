from flask import Flask
from werkzeug import serving
import ssl
import sys

HTTPS_ENABLED = True
VERIFY_USER = True

API_HOST = "0.0.0.0"
API_PORT = 5001
API_CRT = "server_cert.pem"
API_KEY = "server_key.pem"
API_CA_T = "server_cert.pem"

app = Flask(__name__)

@app.route("/")
def main():
    return "Top-level content"

if __name__ == "__main__":
    context = None
    if HTTPS_ENABLED:
        context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        if VERIFY_USER:
            context.verify_mode = ssl.CERT_REQUIRED
            context.load_verify_locations(API_CA_T)
        try:
            context.load_cert_chain(API_CRT, API_KEY)
        except Exception as e:
            sys.exit("Error starting flask server. " + "Missing cert or key. Details: {}".format(e))
    serving.run_simple(API_HOST, API_PORT, app, ssl_context=context)