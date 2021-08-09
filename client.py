import sys, socket, yaml, json

config = yaml.safe_load(open('config.yaml', 'r').read())

if len(sys.argv) == 1:
    print 'command must be provided'
    sys.exit()

if sys.argv[1] in ['get', 'update']:
    hostlist = [sys.argv[2]] if len(sys.argv) >= 3 else config['hosts']
    for host in hostlist:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, 85))
            s.send(json.dumps({
                'command': sys.argv[1],
                'module': sys.argv[3] if len(sys.argv) >= 4 else None,
                'package': sys.argv[4] if len(sys.argv) >= 5 else None
            }).encode())
            data = json.loads(s.recv(102400).decode())
            s.close()    
            for module in data.keys():
                for package in data[module]:
                    if sys.argv[1] == 'get':
                        if package['current'] == package['available']:
                            print '\033[0;32m%s %s %s (%s)' % (host, module, package['name'], package['current'])
                        else:
                            print '\033[0;31m%s %s %s (%s => %s)' % (host, module, package['name'], package['current'], package['available'])
                    elif sys.argv[1] == 'update':
                        if package['current'] == package['available']:
                            print '\033[0;32mSUCCESS: %s %s %s (%s)' % (host, module, package['name'], package['current'])
                        else:
                            print '\033[0;31mFAILURE: %s %s %s (%s => %s)' % (host, module, package['name'], package['current'], package['available'])
        except socket.error as e:
            print '\033[0;31m%s is not available' % (host)

elif sys.argv[1] == 'update':
    pass

else:
    print 'unknown command \'' + sys.argv[1] + '\''
