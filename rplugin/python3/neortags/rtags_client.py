import re
import subprocess


class RtagsClient:
    def __init__(self):
        pass

    def find_references(self, cur_pos):
        result = self._call_rc("-r {} -e".format(cur_pos))
        return self._split_to_list(result)

    def follow_location(self, cur_pos):
        result = self._call_rc('-f {}'.format(cur_pos))
        return self._split_to_list(result)

    def get_symbol_info(self, cur_pos):
        result = self._call_rc('--symbol-info {}'.format(cur_pos))
        return self._split_to_list(result)

    def get_preprocessed_file(self, path: str) -> str:
        result = self._call_rc('--preprocess {}'.format(path))
        return result

    def _call_rc(self, args):
        cmd = 'rc --absolute-path {}'.format(args)
        return subprocess.check_output(cmd, shell=True).decode('utf-8')

    def _split_to_list(self, result):
        return list(filter(None, [re.sub('\s+', ' ', s) for s in result.split('\n')]))
