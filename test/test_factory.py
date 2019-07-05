import context
from di.factory import Factory, VecEnvFactory, get_objects
import os


def test_get():
    args = {
        "salt": 2.4,
        "pepper": "black"
    }

    factory = Factory("dummy.Blubb", args)

    obj = factory.get()
    print(obj)
    assert obj.salt == 2.4
    assert obj.pepper == 'black'


def test_get_vec_env():
    args = [{
        "name": "dummy.DummyEnv",
        "blubb": 22.929
    }]
    factory = VecEnvFactory(
        "stable_baselines.common.vec_env.DummyVecEnv", args)

    obj = factory.get()
    assert obj.envs[0].blubb == 22.929


def test_get_objects_with_factory():
    config = {
        "name": "di.factory.VecEnvFactory",
        "target": "stable_baselines.common.vec_env.DummyVecEnv",
        "args": [
            {
                "name": "dummy.DummyEnv",
                "blubb": 22.929
            }
        ]
    }

    obj = get_objects(config)
    print(obj)

    assert obj.envs[0].blubb == 22.929


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
    print(obj)
    assert obj.bla == 1.03
    assert obj.blubb.salt == 2.4
    assert obj.blubb.pepper == 'black'
    assert obj.summary(something="eintyp") == "eintyp 1.03 2.4 black"
