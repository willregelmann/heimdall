import sys, socket, thread, importlib, json, yaml
from thread import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

config = yaml.safe_load(open('config.yaml', 'r').read())

modules = {}

for service in config['services'].keys():
    modules[service] = importlib.import_module('modules.' + service)

try:
    s.bind(('', config['server']['port']))
except socket.error as e:
    print(str(e))

s.listen(5)
print('Listening...')
def threaded_client(conn):
    ingress = json.loads(conn.recv(2048).decode())
    if ingress['command'] in ['get', 'update']:
        egress = {}
        servicelist = [ingress['module']] if ingress['module'] else config['services'].keys()
        for service in servicelist:
            srv = getattr(modules[service], service)()
            egress[service] = []
            packagelist = [ingress['package']] if ingress['package'] else config['services'][service]
            for package in packagelist:
                if ingress['command'] == 'get':
                    egress[service].extend(srv.get(package))
                elif ingress['command'] == 'update':
                    egress[service].extend(srv.update(package))
                    print 'updated %s: %s' % (service, package)
        egressdata = json.dumps(egress).encode()
        egressbytes = 0
        conn.send(str(len(egressdata)).rjust(32, '0'))
        while egressbytes < len(egressdata):
            sent = conn.send(egressdata[egressbytes:])
            egressbytes += sent
    conn.close

while True:
    conn, addr = s.accept()
    print('connected to: '+addr[0]+':'+str(addr[1]))
    if addr[0] in config['server']['authorized_clients']:
        start_new_thread(threaded_client,(conn,))
    else:
        conn.close
