import importlib


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

    obj = getattr(__import__(module), funct)(**args)

    return obj
