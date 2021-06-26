import subprocess
import json

# show IP address
x = subprocess.run('ip -j link', capture_output=True, shell=True)
j=x.stdout.decode()
y=json.loads(j)
print(y[1]['address'])
dname=y[1]['ifname']

# change IP address
mac='08:00:27:ec:c0:c9'
pwd = '12345678'
subprocess.run('echo {} | sudo -S ip link set dev {} down'.format(pwd,dname), shell=True)
x=subprocess.run('echo {} | sudo -S ip link set dev {} address {}'.format(pwd,dname,mac), shell=True)
subprocess.run('echo {} | sudo -S ip link set dev {} up'.format(pwd,dname), shell=True)