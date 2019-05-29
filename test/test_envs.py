import context
from rltrader import env as rlenvs
from rltrader import spaces as rlspaces
from gym import spaces
import pandas as pd
import numpy as np


def get_env(space):
    return rlenvs.Env(space=space)


def get_data_space(lookback, action_space):
    df = pd.DataFrame([{'feature1': 7, 'feature2': 52},
                       {'feature1': 4, 'feature2': 90},
                       {'feature1': 10, 'feature2': 100},
                       {'feature1': 6, 'feature2': 75},
                       {'feature1': 2, 'feature2': 0},
                       {'feature1': 1, 'feature2': 9}])
    space = rlspaces.DataSpace(action_space=action_space, history_lookback=lookback,
                               data=df)
    return space


def test_space():
    action_space = spaces.Discrete(2)
    observation_space = spaces.Box(low=0, high=1, shape=(2, 3))
    space = rlspaces.Space(action_space=action_space,
                           observation_space=observation_space)
    env = get_env(space)

    assert env.action_space == action_space
    assert env.observation_space == observation_space


def test_reset():
    lookback = 3
    action_space = spaces.Discrete(2)

    expected = np.array([[0.5, 0.],
                         [0., 0.79166667],
                         [1., 1.],
                         [0.33333333, 0.47916667]])
    space = get_data_space(lookback, action_space)
    env = get_env(space)
    actual = env.reset()
    assert np.allclose(actual, expected)


def test_step():
    lookback = 3
    action_space = spaces.Discrete(2)

    expected = np.array([[0.5, 0.],
                         [0., 0.79166667],
                         [1., 1.],
                         [0.33333333, 0.47916667]])
    space = get_data_space(lookback, action_space)
    env = get_env(space)

    action = 1
    obs, reward, done, info = env.step(action)

    assert reward == 0
    assert done == False
    assert info == {}
    assert np.allclose(obs, expected)


def test_step_done():
    lookback = 3
    action_space = spaces.Discrete(2)

    space = get_data_space(lookback, action_space)
    env = get_env(space)

    for n in range(5):
        obs, reward, done, info = env.step(1)
    assert done
