from gym import Env as BaseEnv
from gym import spaces


class Dummy:
    def __init__(self, blubb, bla=2, something=3):
        self.bla = bla
        self.blubb = blubb

    def summary(self, something):
        return "{} {} {} {}".format(something, self.bla, self.blubb.salt, self.blubb.pepper)


class Blubb:

    def __init__(self, salt=2, pepper='white'):
        self.salt = salt
        self.pepper = pepper


class DummyEnv(BaseEnv):
    def __init__(self, blubb):
        self.blubb = blubb
        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(
            low=0, high=1, shape=(2, 5))
