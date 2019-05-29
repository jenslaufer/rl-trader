import context
from rltrader import spaces as rlspaces
from gym import spaces
import pandas as pd
import numpy as np


df = pd.DataFrame([{'feature1': 7, 'feature2': 52},
                   {'feature1': 4, 'feature2': 90},
                   {'feature1': 10, 'feature2': 100},
                   {'feature1': 6, 'feature2': 75},
                   {'feature1': 2, 'feature2': 0},
                   {'feature1': 1, 'feature2': 9}])


def test_spaces():
    action_space = spaces.Discrete(2)
    observation_space = spaces.Box(low=0, high=1, shape=(2, 3))
    space = rlspaces.Space(action_space=action_space,
                           observation_space=observation_space)
    assert space.action_space == action_space
    assert space.observation_space == observation_space


def get_space(action_space, lookback, random_start, seed):
    return rlspaces.DataSpace(action_space=action_space, history_lookback=lookback,
                              data=df, random_start=random_start, seed=seed)


def test_data_space_reset_unrandom():
    action_space = spaces.Discrete(2)
    lookback = 2
    space = get_space(action_space, lookback, False, None)

    assert space.action_space == action_space
    assert space.current_index == (len(df) - lookback)


def test_data_space_reset_random():
    action_space = spaces.Discrete(2)
    lookback = 2
    space = get_space(action_space, lookback, True, 9)

    assert space.action_space == action_space
    assert space.current_index == 5


def test_next_observation():
    action_space = spaces.Discrete(2)
    lookback = 2
    space = get_space(action_space, lookback, True, 9)

    expected0 = np.array(
        [[1., 1.], [0.5, 0.75], [0., 0.]]).astype('float64')
    obs = space.next_observation()
    assert np.array_equal(obs, expected0)

    expected1 = np.array(
        [[1., 1.], [0.2, 0.], [0., 0.12]]).astype('float64')
    obs = space.next_observation()

    print(type(obs.dtype))
    print(type(expected1.dtype))
    assert np.allclose(obs, expected1)

    obs = space.next_observation()
    assert obs == None
