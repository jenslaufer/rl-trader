class Context:

    def act(self, action, observation):
        return (0, False)


class DummyContext(Context):

    def __init__(self):
        self.rewards = [8, 2, 3]
        self.contexts = [{"b": "blubb"}, {"b": "blabb"}, {"b": "bla"}]
        self.current_index = 0

    def act(self, action, observation):
        done = False
        context = {}
        try:
            reward = self.rewards[self.current_index]
            context = self.contexts[self.current_index]
        except:
            reward = 0
        self.current_index += 1

        return (reward, done, context)
