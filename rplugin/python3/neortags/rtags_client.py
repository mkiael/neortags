
import re
import subprocess

class RtagsClient(object):
    def __init__(self):
        pass

    def _call(self, args):
        cmd = 'rc {}'.format(args)
        return subprocess.check_output(cmd, shell=True).decode('utf-8')

    def req_find_references(self, cur_pos):
        result = self._call("--absolute-path -r {} -e".format(cur_pos))
        return list(filter(None, [re.sub('\s+', ' ', s) for s in result.split('\n')]))
