import re
import subprocess


class RtagsClient:
    def __init__(self):
        pass

    def find_references(self, cur_pos) -> list:
        result = self._call_rc("--references {} --all-references".format(cur_pos))
        return self._split_to_list(result)

    def find_virtuals(self, cur_pos) -> list:
        result = self._call_rc("--references {} --find-virtuals".format(cur_pos))
        return self._split_to_list(result)

    def follow_location(self, cur_pos) -> list:
        result = self._call_rc('--follow-location {}'.format(cur_pos))
        return self._split_to_list(result)

    def get_symbol_info(self, cur_pos) -> list:
        result = self._call_rc('--symbol-info {}'.format(cur_pos))
        return self._split_to_list(result)

    def get_preprocessed_file(self, path: str) -> str:
        result = self._call_rc('--preprocess {}'.format(path))
        return result

    def dump_class_hierarchy(self, cur_pos) -> str:
        result = self._call_rc('--class-hierarchy {}'.format(cur_pos))
        return result

    def include_file(self, path: str, symbol: str) -> str:
        result = self._call_rc('--current-file {file} --include-file {symbol}'.format(file=path, symbol=symbol))
        return result

    def _call_rc(self, args) -> str:
        cmd = 'rc --absolute-path {}'.format(args)
        try:
            return subprocess.check_output(cmd, shell=True).decode('utf-8')
        except subprocess.CalledProcessError:
            return ''

    def _split_to_list(self, result) -> list:
        return list(filter(None, [re.sub('\s+', ' ', s) for s in result.split('\n')]))
