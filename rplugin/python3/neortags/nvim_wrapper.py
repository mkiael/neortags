

class NvimWrapper(object):

    def __init__(self, nvim):
        self._nvim = nvim

    def get_current_pos(self):
        file_path = self._nvim.call('expand', '%')
        lnum, col = self._nvim.call('getcurpos')[1:3]
        return "{}:{}:{}".format(file_path, lnum, col)

    def print_message(self, msg):
        self._nvim.command('echo "%s"' % msg)
