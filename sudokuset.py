class SudokuSet(set):
    def __init__(self, s=0, foo=None):
        super(SudokuSet,self).__init__()
        
        if foo is None and hasattr(s, 'foo'):
            foo = s.foo
        self.foo = foo
        
        if 0 == s:
            for x in range(1,10):
                self.add(x)
        else:
            self.add(s)
     
    def discard(self, n):
        ''' Discard n only if it isn't the only value. '''
        if isinstance(n, set) and len(self) > 1:
            self -= n
    
    def get_solution(self):
        ''' Returns single int or '-' if multiples. '''
        if 1 == len(self):
            for x in self:
                return int(x)
        else:
            return '-'

    @classmethod
    def _wrap_methods(cls, names):
        def wrap_method_closure(name):
            def inner(self, *args):
                result = getattr(super(cls, self), name)(*args)
                if isinstance(result, set) and not hasattr(result, 'foo'):
                    result = cls(result, foo=self.foo)
                return result
            inner.fn_name = name
            setattr(cls, name, inner)
        for name in names:
            wrap_method_closure(name)

# Methods listed here pass right thru to super
SudokuSet._wrap_methods(['__ror__', 'difference_update', '__isub__', 
    'symmetric_difference', '__rsub__', '__and__', '__rand__', 'intersection',
    'difference', '__iand__', 'union', '__ixor__', 
    'symmetric_difference_update', '__or__', 'copy', '__rxor__',
    'intersection_update', '__xor__', '__ior__', '__sub__', #'discard',
])