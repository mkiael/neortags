import neovim

@neovim.plugin
class Neortags(object):
    def __init__(self, vim):
        self.vim = vim

    @neovim.function('NeortagsTest')
    def neortags_test(self):
        self.vim.command('echo "From neortags_test"')
