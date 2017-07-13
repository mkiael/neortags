import json


class NvimWrapper(object):


    def __init__(self, nvim):
        self._nvim = nvim


    def get_current_pos(self):
        file_path = self._nvim.call('expand', '%')
        lnum, col = self._nvim.call('getcurpos')[1:3]
        return "{}:{}:{}".format(file_path, lnum, col)


    def display_result(self, result):
        location_list = self._parse_result(result)
        if len(location_list) > 0:
            win_nr = self._nvim.call('winnr')
            self._nvim.call('setloclist', win_nr, location_list)
            self._nvim.command('lopen')


    def jump_to(self, result_str):
        file_path, lnum, col, description = self._parse_result_str(result_str)
        if file_path != self._nvim.call('expand', '%:p'):
            self._nvim.command('e {}'.format(file_path))
        self._nvim.call('cursor', lnum, col)


    def print_message(self, msg):
        self._nvim.command('echo "%s"' % msg)


    def _parse_result(self, result):
        location_list = []
        for s in result:
            file_path, lnum, col, description = self._parse_result_str(s)
            entry = {'filename': file_path, 'lnum': lnum, 'col': col, 'text': description}
            location_list.append(entry)
        return location_list


    def _parse_result_str(self, s):
        location, description = s.split(' ', 1)
        file_path, lnum, col = filter(None, location.split(':'))
        return file_path, lnum, col, description

