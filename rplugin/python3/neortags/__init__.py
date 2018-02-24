import neovim

from .nvim_wrapper import NvimWrapper
from .rtags_client import RtagsClient


@neovim.plugin
class Neortags:
    def __init__(self, nvim):
        self._nvim = NvimWrapper(nvim)
        self._rtags_client = RtagsClient()

    @neovim.command(name='NeortagsFindReferences', sync=False)
    def find_references(self):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.find_references(cur_pos)
        self._nvim.display_in_qf_or_loclist(result)

    @neovim.command(name='NeortagsFindVirtuals', sync=False)
    def find_virtuals(self):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.find_virtuals(cur_pos)
        self._nvim.display_in_qf_or_loclist(result)

    @neovim.command(name='NeortagsJumpTo', sync=False)
    def jump_to(self):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.follow_location(cur_pos)
        if len(result) > 1:
            self._nvim.display_in_qf_or_loclist(result)
        elif len(result) == 1:
            self._nvim.jump_to(result[0])

    @neovim.command(name='NeortagsSymbolInfo', sync=False)
    def symbol_info(self):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.get_symbol_info(cur_pos)
        self._nvim.print_message('\n'.join(result))

    @neovim.command(name='NeortagsPreprocess', sync=False)
    def preprocess(self):
        path = self._nvim.current_path
        result = self._rtags_client.get_preprocessed_file(path)
        self._nvim.display_in_preview(result)

    @neovim.command(name='NeortagsFindIncludeFile', sync=False, nargs=1)
    def find_include_file(self, args):
        if args:
            symbol = args[0]
            path = self._nvim.current_path
            result = self._rtags_client.include_file(path, symbol) or "No include found"
            self._nvim.print_message(result)
        else:
            self._nvim.print_message("Must give an argument")

    @neovim.command(name='NeortagsClassHierarchy', sync=False)
    def class_hierarchy(self):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.dump_class_hierarchy(cur_pos)
        if result:
            self._nvim.display_in_preview(result)
        else:
            self._nvim.print_message('Could not find class hierarchy')
