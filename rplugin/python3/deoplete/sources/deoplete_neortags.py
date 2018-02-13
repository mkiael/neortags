from .base import Base

class Source(Base):

    def __init__(self, vim):
        Base.__init__(self, vim)
        self.name = 'neortags'
        self.mark = '[neortags]'
        self.filetypes = ['c', 'cpp']
        self.rank = 500
        self.input_pattern = (r'[^. \t0-9]\.\w*|'
                              r'[^. \t0-9]->\w*|'
                              r'[a-zA-Z_]\w*::\w*')

    def gather_candidates(self, context):
        return ['foo', 'bar']