import context
from rltrader import spaces as rlspaces
from gym import spaces


def test_spaces():
    action_space = spaces.Discrete(2)
    observation_space = spaces.Box(low=0, high=1, shape=(2, 3))
    space = rlspaces.Space(action_space=action_space,
                           observation_space=observation_space)
    assert space.action_space == action_space
    assert space.observation_space == observation_space
