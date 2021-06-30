from flask import Blueprint, request, jsonify
network = Blueprint('network',__name__)
import ssl, os, sys, subprocess, json

def sudo(cmd):
    pwd = '12345678'
    subprocess.run('echo {} | sudo -S {}'.format(pwd,cmd),shell=True)

@network.route("/mac",methods=['GET','POST'])
def mac():
    if request.method=='GET':
        x = subprocess.run('ip -j link', capture_output=True, shell=True)
        j=x.stdout.decode()
        y=json.loads(j)
        return jsonify(y[1]['address'])
    elif request.method=='POST':
        dname='enp0s3'
        sudo(f'ip link set dev {dname} down')
        sudo(f'ip link set dev {dname} address {request.json["mac"]}')
        sudo(f'ip link set dev {dname} up')
        return jsonify('MAC Address changed successfully!')

@network.route('/ip',methods=['GET','POST'])
def ip():
    if request.method=='GET':
        x = subprocess.run('hostname -i', capture_output=True, shell=True)
        return jsonify(x.stdout.decode())
    elif request.method=='POST':
        dname='enp0s3'
        sudo(f'nmcli device modify {dname} ipv4.address {request.json["ip"]}')
        return jsonify('IP Address added successfully!')
