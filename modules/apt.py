from subprocess import Popen, PIPE
import sys, re, json

class apt:
    def __init__(self):
        Popen(['apt', 'update'], stdout=PIPE, stderr=PIPE).wait()
    def get(self, name):
        data = []
        process = Popen(['apt', 'list', '--installed', name], stdout=PIPE, stderr=PIPE)
        out, err = process.communicate()
        packages = out.splitlines()
        packages.pop(0)
        for package in packages:
            match = re.search('^(\S+)\/\S+\s(\S+).+\[(.*)\]$', package)
            name = match.group(1)
            current = match.group(2)            
            match = re.search('upgradable\sto:\s(.+)$', match.group(3))
            available = match.group(1) if match else current
            data.append({
                'name': name, 
                'current': current,
                'available': available
            })
        return data
    def update(self, name):
        data = []
        initial = self.get(name)
        Popen(['apt', 'update'], stdout=PIPE, stderr=PIPE).wait()
        Popen(['apt', '--only-upgrade', 'install', '-y', name], stdout=PIPE, stderr=PIPE).wait()
        final = self.get(name)
        for old in initial:
            if old['current'] == old['available']:
                continue
            for new in final:
                if old['name'] == new['name']:
                    data.append({
                        'name': new['name'],
                        'current': new['current'],
                        'available': new['available']
                    })
        return data
