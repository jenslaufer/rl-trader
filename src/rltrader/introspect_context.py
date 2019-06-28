
from rltrader.util.introspect import list_module_content, introspect_constructor
import json


def do_introspect():
    modules = {'stable_baselines.common.policies',
               'rltrader', 'stable_baselines'}
    for module in modules:
        summary = []
        clazzes = list_module_content(module)
        print(clazzes)
        for clazz in clazzes:
            module_name = "{}.{}".format(module, clazz)
            details = {}
            try:
                args, defaults = introspect_constructor(module_name)
                details = {"module": module_name}
                for arg in args:
                    try:
                        default = defaults[arg]
                    except:
                        default = None
                    details[arg] = default

            except:
                pass
            summary.append(details)

        with open('{}.json'.format(module), 'w') as f:
            json.dump(summary, f, ensure_ascii=False)


if __name__ == '__main__':
    do_introspect()
