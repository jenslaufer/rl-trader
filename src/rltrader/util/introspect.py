from importlib import import_module
import inspect


def introspect_constructor(module_name):
    module, funct = split_module_class(module_name)

    try:
        spec = inspect.getargspec(
            getattr(import_module(module), funct).__init__)
    except Exception as e:
        spec = inspect.getargspec(getattr(import_module(module), funct))

    defaults = {}
    if spec.defaults != None:
        defaults = dict(zip(spec.args[-len(spec.defaults):], spec.defaults))

    return spec.args[1:], defaults


def list_module_content(module_name):
    return [i for i in dir(import_module(module_name)) if "__" not in i]


def split_module_class(module_name):
    try:
        index = module_name.rindex(".")
        module = module_name[:index]
        funct = module_name[index+1:]

        return module, funct
    except Exception as e:
        print("problem splitting {}: {}".format(module_name, e))


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

    return getattr(import_module(module), funct)(**args)
