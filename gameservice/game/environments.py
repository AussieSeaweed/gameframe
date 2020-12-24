"""
This module defines environments in gameservice.
"""
from abc import ABC


class Environment(ABC):
    """
    This is a class that represents environments.
    """

    def __init__(self, game):
        self.__game = game

    @property
    def game(self):
        """
        :return: the game of the environment
        """
        return self.__game
