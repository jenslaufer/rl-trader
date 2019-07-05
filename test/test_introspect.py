import context
from di.introspect import split_module_class, \
    introspect_constructor, list_module_content


def test_split_module_class():
    module, name = split_module_class(
        "stable_baselines.common.policies.MlpPolicy")

    assert module == "stable_baselines.common.policies"
    assert name == "MlpPolicy"


def test_list_module_content():
    content = list_module_content("dummy")

    assert content == ['BaseEnv', 'Blubb', 'Dummy', 'DummyEnv', 'spaces']


def test_introspect():
    args, defaults = introspect_constructor("dummy.Dummy")

    assert args == ['blubb', 'bla', 'something']
    assert defaults == {'bla': 2, 'something': 3}
