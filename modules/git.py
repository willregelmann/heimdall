from subprocess import Popen, PIPE
import sys, re, json

class git:
    def __init__(self):
        pass
    def get(self, path):
        out, err = Popen(['git', '-C', path, 'remote', '-v'], stdout=PIPE, stderr=PIPE).communicate()
        name = re.search('^\S+\s+(\S+)', out.splitlines()[0]).group(1)
        out, err = Popen(['git', '-C', path, 'log'], stdout=PIPE, stderr=PIPE).communicate()
        current = re.search('^commit\s(\S+)', out.splitlines()[0]).group(1)
        Popen(['git', '-C', path, 'fetch'], stdout=PIPE, stderr=PIPE).wait()
        out, err = Popen(['git', '-C', path, 'log', 'FETCH_HEAD'], stdout=PIPE, stderr=PIPE).communicate()
        available = re.search('^commit\s(\S+)', out.splitlines()[0]).group(1)
        return [{
            'name': name,
            'current': current,
            'available': available
        }]
    def update(self, path):
        data = []
        info = self.get(path)[0]
        if info['current'] == info['available']:
            return []
        Popen(['git', '-C', path, 'pull']).wait()
        return self.get(path)
