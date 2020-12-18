"""
This module defines a general game test in gameservice.
"""
from abc import ABC, abstractmethod
from random import choice


class GameTestCaseMixin(ABC):
    """
    This is a mixin for all game test cases in gameservice.
    """

    @staticmethod
    @abstractmethod
    def create_game():
        """
        Creates a game instance.
        :return: a game instance
        """
        pass

    @staticmethod
    @abstractmethod
    def check_game(game):
        """
        Checks the integrity of the game.
        :param game: a game to be checked on
        :return: None
        """
        pass


class SeqTestCaseMixin(GameTestCaseMixin, ABC):
    """
    This is a mixin for all sequential game test cases in gameservice.
    """

    @property
    @abstractmethod
    def num_monte_carlo_tests(self):
        """
        Returns the number of monte carlo tests of sequential games.
        :return: the number of monte carlo tests of sequential games
        """
        pass

    def test_monte_carlo(self):
        """
        Runs monte carlo tests of sequential games.
        :return: None
        """
        for i in range(self.num_monte_carlo_tests):
            game = self.create_game()

            while not game.terminal:
                choice(game.player.actions).act()

            assert self.check_game(game)