#coding:utf-8

from .util import args_passer, kwargs_passer

class ArrowComposableCallable:
    def __init__(self, f, args_wrapper=None):
        if isinstance(f, ArrowComposableCallable):
            # prevent Russian doll nesting
            f = f._f
        self._f = f
        self._wrapper = args_wrapper
        self.__name__ = f.__name__
        #if callable(args_wrapper):
        #    print("{} wraps output with {}".format(self.__name__, args_wrapper.__name__))
        
    def __call__(self, *args, **kwargs):
        #print ("{} takes args {} and kwargs {}".format(self.__name__, args, kwargs))
        return self._f(*args, **kwargs)
    
    def __rshift__(self, g):
        if not isinstance(self, ArrowComposableCallable) or self._wrapper is None:
            def composed(*args, **kwargs):
                return g(self(*args, **kwargs))
        else:
            wrapper = self._wrapper
            def composed(*args, **kwargs):
                a, kw = wrapper(self(*args, **kwargs))
                return g(*a, **kw)
        composed.__name__ = "{} >> {}".format(self.__name__, g.__name__)
        
        w = None if not isinstance(g, ArrowComposableCallable) else g._wrapper
        #print("({})>>({}) -> {}".format(self.__name__, g.__name__, composed.__name__), end="")
        #print(" with {}".format(w.__name__)) if callable(w) else print()
        return ArrowComposableCallable(composed, w)
    
    def __rrshift__(self, f):
        # f >> self
        #print("{} __rrshift__ {}".format(self.__name__, f.__name__))
        return ArrowComposableCallable.__rshift__(f, self)

