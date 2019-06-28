import context
from rltrader.util.introspect import split_module_class, get_objects, introspect_constructor


def test_split_module_class():
    module, name = split_module_class(
        "stable_baselines.common.policies.MlpPolicy")

    assert module == "stable_baselines.common.policies"
    assert name == "MlpPolicy"


def test_get_objects():
    config = {"name": "dummy.Dummy",
              'bla': 1.03,
              'something': 2.9,
              'blubb': {"name": "dummy.Blubb",
                        "salt": 2.4,
                        "pepper": "black"
                        }
              }

    obj = get_objects(config)

    assert obj.bla == 1.03
    assert obj.blubb.salt == 2.4
    assert obj.blubb.pepper == 'black'


def test_introspect():
    args, defaults = introspect_constructor("dummy.Dummy")

    assert args == ['blubb', 'bla', 'something']
    assert defaults == {'bla': 2, 'something': 3}
