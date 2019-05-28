import context
from rltrader import env as rlenvs
from rltrader import spaces as rlspaces
from gym import spaces
import pandas as pd


def get_env(space):
    return rlenvs.Env(space=space)


def test_space():
    action_space = spaces.Discrete(2)
    observation_space = spaces.Box(low=0, high=1, shape=(2, 3))
    space = rlspaces.Space(action_space=action_space,
                           observation_space=observation_space)
    env = get_env(space)

    assert env.action_space == action_space
    assert env.observation_space == observation_space


def test_space2():
    lookback = 3
    action_space = spaces.Discrete(2)
    df = pd.DataFrame([{'feature1': 12, 'feature2': 56}, {
                      'feature1': 14, 'feature2': 44}, {'feature1': 11, 'feature2': 39}])
    space = rlspaces.DataSpace(action_space=action_space, lookback=lookback,
                               data=df)
    env = get_env(space)

    assert env.action_space == action_space
    assert len(df.columns) == 2
    assert env.observation_space == spaces.Box(
        low=0, high=1, shape=(len(df.columns), lookback + 1))


def test_reset():
    action_space = spaces.Discrete(2)
    observation_space = spaces.Box(low=0, high=1, shape=(2, 3))
    space = rlspaces.Space(action_space=action_space,
                           observation_space=observation_space)
    env = get_env(space)

    assert env.reset() == None


def test_step():
    action_space = spaces.Discrete(2)
    observation_space = spaces.Box(low=0, high=1, shape=(2, 3))
    space = rlspaces.Space(action_space=action_space,
                           observation_space=observation_space)
    env = get_env(space)
    action = 1
    obs, reward, done, info = env.step(action)

    assert obs == None
    assert reward == 0
    assert done == False
    assert info == {}
