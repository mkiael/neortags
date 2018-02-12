import neovim

from .nvim_wrapper import NvimWrapper
from .rtags_client import RtagsClient


@neovim.plugin
class Neortags:
    def __init__(self, nvim):
        self._nvim = NvimWrapper(nvim)
        self._rtags_client = RtagsClient()

    @neovim.function(name='NeortagsFindReferences', sync=True)
    def find_references(self, args):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.find_references(cur_pos)
        self._nvim.display_in_qf_or_loclist(result)

    @neovim.function(name='NeortagsJumpTo', sync=True)
    def jump_to(self, args):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.follow_location(cur_pos)
        if len(result) > 1:
            self._nvim.display_in_qf_or_loclist(result)
        elif len(result) == 1:
            self._nvim.jump_to(result[0])

    @neovim.function(name='NeortagsSymbolInfo', sync=True)
    def symbol_info(self, args):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.get_symbol_info(cur_pos)
        self._nvim.print_message('\n'.join(result))

    @neovim.function(name='NeortagsPreprocess', sync=True)
    def preprocess(self, args):
        path = self._nvim.current_path
        result = self._rtags_client.get_preprocessed_file(path)
        self._nvim.display_in_preview(result)
