#coding:utf-8

from .util import args_passer, kwargs_passer, build_wrapper
from .composable import ArrowComposableCallable

class InfixFunctionComposer:
    def __init__(self):
        self._f_cache = None
        self._wrapper_cache = None
    
    def __rshift__(comp, g):
        #print("({})>>({}) -> o".format('o', g.__name__))
        # because >> takes precedence over |
        # we need to return a thing with a __ror__ which takes
        # f and returns g o f
        # that thing is me; just set my _f_cache to g
        comp._f_cache = g
        return comp
    
    def __ror__(comp, f):
        wrapper = comp._wrapper_cache
        comp._wrapper_cache = None
        g = comp._f_cache
        comp._f_cache = None
        
        f = ArrowComposableCallable(f, wrapper)
        # now this thing can just use >> rather than |o>>
        h = f >> g
        #print("({})|({}) -> {}".format(g.__name__, 'o', h.__name__))
        return h
    
    def __getitem__(comp, wrapper_config):
        wrapper = build_wrapper(wrapper_config)
        comp._wrapper_cache = wrapper
        return comp
    
    @staticmethod
    def __rpow__(f):
        #print("({})**({}) -> {}".format(f.__name__, 'o', f.__name__))
        #print("{} passes output with kwargs_passer".format(f.__name__))
        return ArrowComposableCallable(f, kwargs_passer)
    
    @staticmethod
    def __rmul__(f):
        #print("({})*({}) -> {}".format(f.__name__, 'o', f.__name__))
        #print("{} passes output with args_passer".format(f.__name__))
        return ArrowComposableCallable(f, args_passer)


o = InfixFunctionComposer()

