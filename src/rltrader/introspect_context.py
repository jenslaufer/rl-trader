
from rltrader.util.introspect import list_module_content, introspect_constructor
import json
from inspect import isfunction


def do_introspect():
    modules = {'stable_baselines.common.policies',
               'rltrader.context', 'rltrader.rewards', 'rltrader.spaces', 'rltrader.env', 'stable_baselines'}
    for module in modules:
        summary = []
        clazzes = list_module_content(module)
        # print(clazzes)
        for clazz in clazzes:
            module_name = "{}.{}".format(module, clazz)
            details = {}
            try:
                args, defaults = introspect_constructor(module_name)
                details = {"module": module_name}
                for arg in args:
                    try:
                        default = defaults[arg]
                        if isfunction(default):
                            default = default.__name__
                    except Exception as e:
                        print("e1: {}".format(e))
                        default = None
                    details[arg] = default

            except Exception as e:
                print("e2: {}".format(e))
            summary.append(details)

        with open('{}.json'.format(module), 'w') as f:
            json.dump(summary, f, ensure_ascii=False)


if __name__ == '__main__':
    do_introspect()
