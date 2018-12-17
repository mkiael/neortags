import pynvim


class NvimWrapper:
    def __init__(self, nvim: pynvim.Nvim):
        self._nvim = nvim

    @property
    def use_qf(self) -> bool:
        use_qf = bool(self._nvim.vars.get('neortags_use_qf', False))
        return use_qf

    @property
    def current_path(self) -> str:
        file_path = self._nvim.call('expand', '%:p')
        return file_path

    def get_current_pos(self):
        file_path = self.current_path
        lnum, col = self._nvim.call('getcurpos')[1:3]
        return "{}:{}:{}".format(file_path, lnum, col)

    def display_in_qf_or_loclist(self, result):
        result_list = self._parse_result(result)
        if len(result_list) > 0:
            if self.use_qf:
                self._nvim.call('setqflist', result_list)
                self._nvim.command('copen')
            else:
                win_nr = self._nvim.call('winnr')
                self._nvim.call('setloclist', win_nr, result_list)
                self._nvim.command('lopen')

    def display_in_preview(self, text: str):
        if text:
            self._nvim.command("pedit! Preview | wincmd P | wincmd L")
            self._nvim.current.buffer[:] = text.splitlines()

            self._nvim.current.buffer.options['buftype'] = 'nofile'
            self._nvim.current.buffer.options['bufhidden'] = 'wipe'
            self._nvim.current.buffer.options['buflisted'] = False
            self._nvim.current.window.options['spell'] = False
            self._nvim.current.window.options['foldenable'] = False
            self._nvim.current.window.options['colorcolumn'] = ''
            self._nvim.current.window.options['cursorline'] = True
            self._nvim.current.window.options['cursorcolumn'] = False

    def jump_to(self, result_str):
        file_path, lnum, col, description = self._parse_result_str(result_str)
        self._nvim.command("normal! m`")
        if file_path != self._nvim.call('expand', '%:p'):
            self._nvim.command('e {}'.format(file_path))
        self._nvim.call('cursor', lnum, col)

    def print_message(self, msg):
        self._nvim.command('echo \'{}\''.format(msg))

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
