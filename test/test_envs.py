import context
from rltrader import env as rlenvs
from rltrader import spaces as rlspaces
from rltrader import context as rlcontext
from gym import spaces
import pandas as pd
import numpy as np


class DummyContext(rlcontext.Context):

    def __init__(self):
        self.done = [False, True, True]
        self.context_data = [{"bla": 1}, {"bla": 2}, {"bla": 3}, {"bla": 4}, ]
        self.current_index = 0

    def act(self, action, observation):
        done = self.done[self.current_index]
        old_state = self.context_data[self.current_index]
        self.current_index += 1
        current_state = self.context_data[self.current_index]

        return done, old_state, current_state, observation

    def reset(self):
        self.current_index = 0


def dummy(old_context, new_context, action, obs, done):
    return 23


def get_context():
    return DummyContext()


def get_env(space, context):
    return rlenvs.Env(space=space, context=context, reward=dummy)


def get_data_space(lookback, action_space):
    df = pd.DataFrame([{'feature1': 7, 'feature2': 52},
                       {'feature1': 4, 'feature2': 90},
                       {'feature1': 10, 'feature2': 100},
                       {'feature1': 6, 'feature2': 75},
                       {'feature1': 2, 'feature2': 0},
                       {'feature1': 1, 'feature2': 9}])
    space = rlspaces.LookbackWindowDataSpace(action_space=action_space, history_lookback=lookback,
                                             data=df)
    return space


def test_space():
    action_space = spaces.Discrete(2)
    observation_space = spaces.Box(low=0, high=1, shape=(2, 3))
    space = rlspaces.Space(action_space=action_space,
                           observation_space=observation_space)
    context = get_context()
    env = get_env(space, context)

    assert env.action_space == action_space
    assert env.observation_space == observation_space


def test_reset():
    lookback = 3
    action_space = spaces.Discrete(2)

    space = get_data_space(lookback, action_space)
    context = get_context()
    env = get_env(space, context)

    expected = np.array([[0.5, 0.],
                         [0., 0.79166667],
                         [1., 1.],
                         [0.33333333, 0.47916667]])
    actual = env.reset()
    assert np.allclose(actual, expected)


def test_step():
    lookback = 3
    action_space = spaces.Discrete(2)

    space = get_data_space(lookback, action_space)
    context = get_context()
    env = get_env(space, context)

    expected = np.array([[0.5, 0.],
                         [0., 0.79166667],
                         [1., 1.],
                         [0.33333333, 0.47916667]])
    action = 1
    obs, reward, done, info = env.step(action)
    assert reward == 23
    assert done == False
    assert info == {'bla': 2, 'reward': 23, 'action': 1, 'done': False}
    assert np.allclose(obs, expected)

    expected = np.array([[0.25, 0.9],
                         [1., 1.],
                         [0.5, 0.75],
                         [0., 0.]])

    action = 1
    obs, reward, done, info = env.step(action)

    assert reward == 23
    assert done == True
    assert info == {'bla': 3, 'reward': 23, 'action': 1, 'done': True}
    assert np.allclose(obs, expected)


def test_step_done():
    lookback = 3
    action_space = spaces.Discrete(2)

    space = get_data_space(lookback, action_space)
    context = get_context()
    env = get_env(space, context)

    for n in range(3):
        obs, reward, done, info = env.step(1)
    assert done


def test_history():
    lookback = 3
    action_space = spaces.Discrete(2)

    space = get_data_space(lookback, action_space)
    context = get_context()
    env = get_env(space, context)
    action = 1
    obs, reward, done, info = env.step(action)
    action = 1
    obs, reward, done, info = env.step(action)

    assert env.states == [{'bla': 1},
                          {'bla': 2, 'reward': 23, 'action': 1, 'done': False},
                          {'bla': 3, 'reward': 23, 'action': 1, 'done': True}]
