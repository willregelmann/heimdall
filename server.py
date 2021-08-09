import sys, socket, thread, importlib, json, yaml
from thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

config = yaml.safe_load(open('config.yaml', 'r').read())['server']

modules = {}

for module in config['packages'].keys():
    modules[module] = importlib.import_module('modules.' + module)

try:
    s.bind(('', config['port']))
except socket.error as e:
    print(str(e))

s.listen(5)
def threaded_client(conn):
    ingress = json.loads(conn.recv(2048).decode())
    if ingress['command'] in ['get', 'update', 'getall']:
        egress = {}
        modulelist = [ingress['module']] if ingress['module'] else config['packages'].keys()
        for module in modulelist:
            service = getattr(modules[module], module)()
            egress[module] = []
            packagelist = [ingress['package']] if ingress['package'] else config['packages'][module]
            for package in packagelist:
                if ingress['command'] in ['get', 'getall']:
                    egress[module].extend(service.get(package))
                elif ingress['command'] == 'update':
                    egress[module].extend(service.update(package))
        egressdata = json.dumps(egress).encode()
        egressbytes = 0
        conn.send(str(len(egressdata)).rjust(32, '0'))
        while egressbytes < len(egressdata):
            sent = conn.send(egressdata[egressbytes:])
            egressbytes += sent
    conn.close

while True:
    conn, addr = s.accept()
    if addr[0] in config['authorized_clients']:
        start_new_thread(threaded_client,(conn,))
    else:
        conn.close
