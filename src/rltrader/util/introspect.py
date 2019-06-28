import importlib
import inspect


def introspect_constructor(module_name):
    module, funct = split_module_class(module_name)
    spec = inspect.getargspec(getattr(__import__(module), funct).__init__)
    return spec.args[1:], dict(zip(spec.args[-len(spec.defaults):], spec.defaults))


def split_module_class(module_name):
    index = module_name.rindex(".")
    module = module_name[:index]
    funct = module_name[index+1:]

    return module, funct


def get_objects(d):
    args = {}
    module = ""
    funct = ""
    for k, v in d.items():
        if isinstance(v, dict):
            obj = get_objects(v)
            args[k] = obj
        else:
            if k == 'name':
                module, funct = split_module_class(v)
            else:
                args[k] = v

    return getattr(__import__(module), funct)(**args)
