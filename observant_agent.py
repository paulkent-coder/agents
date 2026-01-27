from agents.base import BatchedAgent
from agents.observant_agent_backend.gamestate import Gamestate
from agents.observant_agent_backend.behaviors import chooseAction


class ObservantAgent(BatchedAgent):

    def __init__(self, num_envs, num_actions):
        # Setup goes here
        super().__init__(num_envs, num_actions)
        self.state = []
        for x in range(num_envs):
            self.state.append(Gamestate())

    def batched_step(self, observations, rewards, dones, infos):
        """
        Perform a batched step on lists of environment outputs.

        Each argument is a list of the respective gym output.
        Returns an iterable of actions.
        """

        # Agent Name: Observant Dungeoneer
        # Takes a few quick steps to observe things before each real action
        with open('readme.txt', 'w') as f:
            f.writelines("start")
        actions = []
        for x in range(self.num_envs):
            if dones[x]:
                self.state[x].reset()
            actions.append(chooseAction(self.state[x], observations[x]))
        return actions

    def reset(self):
        for x in range(self.num_envs):
            self.state[x].reset()

    def displayStats(self):
        for x in range(self.num_envs):
            self.state[x].displayStats()
