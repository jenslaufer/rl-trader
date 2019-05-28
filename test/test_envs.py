import context
from rltrader import env as rlenvs
from rltrader import spaces as rlspaces
from gym import spaces


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
