import time

import numpy as np
import pygame
from gymnasium.utils import EzPickle
from gymnasium.vector.utils import spaces
from pettingzoo import AECEnv
from pettingzoo.utils import wrappers

from .board import Board
from pettingzoo.utils.agent_selector import agent_selector


def env(**kwargs):
    env = raw_env(**kwargs)
    env = wrappers.AssertOutOfBoundsWrapper(env)
    env = wrappers.OrderEnforcingWrapper(env)
    return env

class raw_env(AECEnv, EzPickle):
    metadata = {
        "render_modes": ["human", "cmd"],
        "name": "sos_v0",
        "is_parallelizable": False,
        "render_fps": 1,
    }
    def __init__(self,render_mode: str | None = None, screen_height: int | None = 1000, **kwargs):
        super().__init__()
        EzPickle.__init__(self, render_mode, screen_height)
        self.board = Board()

        self.agents = ["player_1", "player_2"]
        self.possible_agents = self.agents[:]

        self.action_spaces = {i: spaces.MultiDiscrete([64,2]) for i in self.agents}

        self.observation_spaces = {
            i: spaces.Dict(
                {
                    "observation": spaces.Box(
                        low=0, high=2, shape=(8, 8, 3), dtype=np.int8
                    ),
                }
            )
            for i in self.agents
        }

        self.rewards = {i: 0 for i in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {"legal_moves": list(range(0, 64))} for i in self.agents}

        self._agent_selector = agent_selector(self.agents)
        self.agent_selection = self._agent_selector.reset()

        self.render_mode = render_mode
        self.screen_height = screen_height
        self.screen = None

        if self.render_mode == "human":
            self.clock = pygame.time.Clock()

    def observation_space(self,agent):
        return self.observation_spaces[agent]

    def action_space(self,agent):
        return self.action_spaces[agent]

    def reset(self,seed=None, options=None):
        # reset environment
        self.board = Board()

        self.agents = self.possible_agents[:]
        self.rewards = {i: 0 for i in self.agents}
        self._cumulative_rewards = {i: 0 for i in self.agents}
        self.terminations = {i: False for i in self.agents}
        self.truncations = {i: False for i in self.agents}
        self.infos = {i: {} for i in self.agents}
        # selects the first agent
        self._agent_selector.reinit(self.agents)
        self._agent_selector.reset()
        self.agent_selection = self._agent_selector.reset()

        if self.screen is None:
            pygame.init()

        if self.render_mode == "human":
            self.screen = pygame.display.set_mode(
                (self.screen_height, self.screen_height)
            )
            pygame.display.set_caption("SOS")
        else:
            self.screen = pygame.Surface((self.screen_height, self.screen_height))

    def observe(self, agent):
        one_hot_encoded = np.eye(3)[self.board.get_board()]
        new_shape = (8, 8, 3)
        observation = one_hot_encoded.reshape(new_shape)
        observation = np.array(observation, dtype=np.int8)


        action_mask = np.where(np.array(self.board.get_board()) == 0, 1, 0)
        return {
            "observation": observation,
        }


    def step(self, action):
        if (
                self.terminations[self.agent_selection]
                or self.truncations[self.agent_selection]
        ):
            return self._was_dead_step(action)
        # play turn
        rew = self.board.make_move(action)


        # update infos
        # list of valid actions (indexes in board)
        # next_agent = self.agents[(self.agents.index(self.agent_selection) + 1) % len(self.agents)]
        next_agent = self._agent_selector.next()

        self.rewards[self.agent_selection] += rew
        self.rewards[next_agent] += rew*-1

        if self.board.check_game_over():
            print("Game Over")
            print(self.board)
            print(self.board.sos_count)
            self.terminations = {i: True for i in self.agents}

        self._cumulative_rewards[self.agent_selection] = 0
        self.agent_selection = next_agent

        self._accumulate_rewards()
        if self.render_mode == "human":
            self.render()

    def render(self,**kwargs):

        if self.render_mode== "human":
            if self.screen is None:
                self.screen = pygame.display.set_mode((self.screen_height, self.screen_height))
            self.screen.fill((255, 255, 255))
            pygame.display.flip()
            self.clock.tick(60)
        elif self.render_mode == "cmd":
            time.sleep(1)
            print(self.board)

    def apply_mask(self,mask):
        """
        Applies a mask to the first dimension (64 elements) of a MultiDiscrete action space.

        Args:
          action_space: A MultiDiscrete action space.
          mask: A NumPy array representing the mask (shape=(64,)).

        Returns:
          A tuple representing the masked action space.
        """

        return np.array([mask],dtype=np.int8),np.array([1 for _ in range(2)],dtype=np.int8)

