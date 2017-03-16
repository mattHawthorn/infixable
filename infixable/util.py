#coding:utf-8

def build_wrapper(wrapper_config):
    if callable(wrapper_config):
        return wrapper_config
    elif isinstance(wrapper_config, (list, tuple)):
        first = wrapper_config[0]
        t = type(first)
        if t in (list, tuple, slice, dict):
            # assume an args, kwargs pattern
            if len(wrapper_config) == 1:
                return arg_builer_map[type(first)](first)
            elif len(wrapper_config) == 2:
                second = wrapper_config[1]
                if t in (list, tuple, slice):
                    return arg_kwarg_builder_map[t](first, second)
                else:
                    t = type(second)
                    return arg_kwarg_builder_map[t](second, first)
            else:
                raise ValueError("if a list or tuple containing collections is passed, it must have one or two items")
        else:
            # assume list of indexes for *args
            wrapper = build_args_tup_wrapper(wrapper_config)
    elif isinstance(wrapper_config, slice):
        wrapper = build_args_slice_wrapper(wrapper_config)
    elif isinstance(wrapper_config, dict):
        # get output at indices/keys, rename to keywords, and pass as **kwargs
        wrapper = build_kwargs_wrapper(wrapper_config)
    else:
        raise TypeError("{} is not an allowable type to specify an output wrapper function".format(type(wrapper_config)))
    return wrapper

            
def build_args_tup_wrapper(idxs):
    def wrapper(out):
        return tuple(out[i] for i in idxs), nulldict
    return wrapper

def build_args_slice_wrapper(sl):
    def wrapper(out):
        return out[sl], nulldict
    return wrapper
    
def build_kwargs_wrapper(idx_key_map):
    def wrapper(out):
        return nulltuple, {name:out[i] for i, name in idx_key_map.items()}
    return wrapper

def build_args_kwargs_tup_wrapper(idxs, idx_key_map):
    def wrapper(out):
        return  (tuple(out[i] for i in idxs), {name:out[i] for i, name in idx_key_map.items()})
    return wrapper

def build_args_kwargs_slice_wrapper(sl, idx_key_map):
    def wrapper(out):
        return out[sl], {name:out[i] for i, name in idx_key_map.items()}
    return wrapper

arg_builer_map = {dict: build_kwargs_wrapper, list: build_args_tup_wrapper, 
                  tuple: build_args_tup_wrapper, slice: build_args_slice_wrapper}
arg_kwarg_builder_map = {tuple: build_args_kwargs_tup_wrapper, list: build_args_kwargs_tup_wrapper,
                         slice: build_args_kwargs_slice_wrapper}

nulldict = {}
def args_passer(out):
    return out, nulldict

nulltuple = ()
def kwargs_passer(out):
    return nulltuple, out

