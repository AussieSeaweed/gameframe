"""
This module defines poker_ games in gameframe.
"""
from abc import ABC, abstractmethod
from itertools import zip_longest

from .environments import PokerEnvironment
from .players import PokerNature, PokerPlayer
from .utils import LazyNoLimit, NoLimit, StandardDeck, StandardEvaluator, Street
from ..game import ParameterException, SequentialGame


class PokerGame(SequentialGame, ABC):
    """
    This is a class that represents poker_ games.

    When a PokerGame instance is created, its deck, evaluator, limit, and streets are also created through the
    invocations of corresponding create methods, which should be overridden by the subclasses. Also, every subclass
    should override the ante, blinds, and starting_stacks properties accordingly.

    The number of players, denoted by the length of the starting_stacks property, must be greater than or equal to 2.
    """

    def __init__(self):
        super().__init__()

        if not len(self.starting_stacks) > 1:
            raise ParameterException('Poker is played by more than 2 players')

        self.__deck = self.create_deck()
        self.__evaluator = self.create_evaluator()
        self.__limit = self.create_limit()
        self.__streets = self.create_streets()

        self._setup()

    def create_environment(self):
        return PokerEnvironment(self)

    def create_nature(self):
        return PokerNature(self)

    def create_player(self):
        return [PokerPlayer(self) for _ in range(len(self.starting_stacks))]

    @property
    def initial_player(self):
        return self.nature

    @property
    def deck(self):
        """
        :return: the deck of the poker_ game
        """
        return self.__deck

    @property
    def evaluator(self):
        """
        :return: the evaluator of the poker_ game
        """
        return self.__evaluator

    @property
    def limit(self):
        """
        :return: the limit of the poker_ game
        """
        return self.__limit

    @property
    def streets(self):
        """
        :return: a list of the streets of the poker_ game
        """
        return self.__streets

    @property
    def street(self):
        """
        :return: the street of the poker_ game
        """
        return self.__streets[0] if self.__streets else None

    def _setup(self):
        blinds = reversed(self.blinds) if len(self.players) == 2 else self.blinds

        for player, starting_stack, blind in zip_longest(self.players, self.starting_stacks, blinds):
            player.stack = starting_stack

            ante = min(self.ante, player.stack)

            player.stack -= ante
            self.environment.pot += ante

            if blind is not None:
                blind = min(blind, player.stack)

                player.stack -= blind
                player.bet += blind

    @property
    @abstractmethod
    def ante(self):
        """
        :return: the ante of the poker_ game
        """
        pass

    @property
    @abstractmethod
    def blinds(self):
        """
        :return: the blinds of the poker_ game
        """
        pass

    @property
    @abstractmethod
    def starting_stacks(self):
        """
        :return: the starting stacks of the poker_ game
        """
        pass

    @abstractmethod
    def create_deck(self):
        """
        Creates a poker_ deck.

        :return: a poker_ deck
        """
        pass

    @abstractmethod
    def create_evaluator(self):
        """
        Creates a poker_ evaluator.

        :return: a poker_ evaluator
        """
        pass

    @abstractmethod
    def create_limit(self):
        """
        Creates a poker_ limit.

        :return: a poker_ limit
        """
        pass

    @abstractmethod
    def create_streets(self):
        """
        Creates poker_ streets.

        :return: a list of poker_ streets
        """
        pass


class NLHEGame(PokerGame, ABC):
    """
    This is a class that represents no-limit texas hold'em games.

    The blinds property should be of length 2 and be sorted.
    """

    def __init__(self):
        super().__init__()

        if len(self.blinds) != 2 or self.blinds[0] >= self.blinds[1]:
            raise ParameterException('The blinds have to be length of 2 and be sorted')

    def create_deck(self):
        return StandardDeck()

    def create_evaluator(self):
        return StandardEvaluator()

    def create_limit(self):
        return NoLimit()

    def create_streets(self):
        return [Street(2, 0), Street(0, 3), Street(0, 1), Street(0, 1)]


class LazyNLHEGame(NLHEGame, ABC):
    """
    This is a class that represents lazy no-limit texas hold'em games.

    Unlike no-limit texas hold'em games, the actions generated by each player only contains minimum and maximum bet
    amount. To bet/raise an amount that is neither minimum or maximum, an AggressiveAction instance should be created
    and used.
    """

    def create_limit(self):
        return LazyNoLimit()
