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

    @neovim.command(name='NeortagsClassHierarchy', sync=False)
    def class_hierarchy(self):
        cur_pos = self._nvim.get_current_pos()
        result = self._rtags_client.dump_class_hierarchy(cur_pos)
        if result:
            self._nvim.display_in_preview(result)
        else:
            self._nvim.print_message('Could not find class hierarchy')

    @neovim.command(name='NeortagsDependencies', sync=False, nargs='?',
                    complete='customlist,NeortagsDependenciesCompleteFunc')
    def dependencies(self, args):
        path = self._nvim.current_path
        if args:
            filter = args[0]
        else:
            filter = ''
        result = self._rtags_client.dependencies(path, filter)
        if result:
            self._nvim.display_in_preview(result)
        else:
            self._nvim.print_message('Could not find file dependencies')

    @neovim.function("NeortagsDependenciesCompleteFunc", sync=True)
    def dependencies_complete_func(self, *args, **kwargs) -> list:
        return ["includes", "included-by", "depends-on", "depended-on", "tree-depends-on", "raw"]
