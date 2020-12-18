"""
This module defines tic tac toe players in gameservice.
"""
from .actions import TTTMarkAction
from .infosets import TTTInfoSet
from ..game import Player


class TTTPlayer(Player):
    """
    This is a class that represents tic tac toe players.
    """

    @property
    def payoff(self):
        """
        :return: the payoff of the tic tac toe player
        """
        if self.game.environment.winner is None:
            return 0 if self.game.terminal else -1
        else:
            return 1 if self.game.environment.winner is self else -1

    @property
    def actions(self):
        """
        :return: a list of actions of the tic tac toe player
        """
        if self.game.player is self:
            return [TTTMarkAction(self, r, c) for r, c in self.game.environment.empty_coords]
        else:
            return []

    @property
    def info_set(self):
        """
        :return: the info-set of the tic tac toe player
        """
        return TTTInfoSet(self)
