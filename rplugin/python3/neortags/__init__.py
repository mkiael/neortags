import neovim

from neortags.nvim_wrapper import NvimWrapper
from neortags.rtags_client import RtagsClient


@neovim.plugin
class Neortags(object):


    def __init__(self, nvim):
        self._nvim = NvimWrapper(nvim)
        self._rtags_client = RtagsClient()


    @neovim.function(name='NeortagsFindReferences', sync=True)
    def find_references(self, args):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.find_references(cur_pos)
        self._nvim.display_result(result)


    @neovim.function(name='NeortagsJumpTo', sync=True)
    def jump_to(self, args):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.follow_location(cur_pos)
        if len(result) > 1:
            self._nvim.display_result(result)
        elif len(result) == 1:
            self._nvim.jump_to(result[0])
