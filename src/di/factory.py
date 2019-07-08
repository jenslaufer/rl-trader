from .introspect import split_module_class
from importlib import import_module
import inspect


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

    try:
        result = getattr(import_module(module), funct)(**args)

        if isinstance(result, Factory):
            result = result.get()

    except Exception as e:
        print("Exception {}".format(e))
        spec = inspect.getargspec(getattr(import_module(module), funct))
        result = getattr(import_module(module), funct)

    return result


class Factory:

    def __init__(self, target, args):
        self.module, self.funct = split_module_class(target)
        self.args = args

    def get(self):
        return getattr(import_module(self.module), self.funct)(**self.args)


class VecEnvFactory(Factory):

    def __init__(self, target, args):
        super(VecEnvFactory, self).__init__(
            target, args)

    def get(self):
        module = getattr(import_module(self.module), self.funct)

        envs = []
        for arg in self.args:
            envs.append(lambda: get_objects(arg))

        return module(envs)


class ModuleFactory(Factory):
    def __init__(self, target, args):
        super(ModuleFactory, self).__init__(
            target, args)

    def get(self):
        return getattr(import_module(self.module), self.funct)

