from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Iterator, List, Optional

from .actions import Action
from .utils import E, G, N, P


class Player(Generic[G, E, N, P], Iterator[P], ABC):
    """Player is the abstract base class for all players."""

    def __init__(self, game: G):
        self.__game: G = game

    @property
    def game(self) -> G:
        """
        :return: the game of the player
        """
        return self.__game

    @property
    def index(self) -> Optional[int]:
        """
        :return: the index of the player
        """
        return None if self.nature else self.game.players.index(self)

    @property
    def information_set(self) -> Dict[str, Any]:
        """
        :return: the information set of the player
        """
        return {
            'game': self.game._information,
            'environment': self.game.environment._information,
            'nature': self.game.nature._private_information if self.nature else self.game.nature._public_information,
            'player': list(map(
                lambda player: player._private_information if self is player else player._public_information,
                self.game.players)),
        }

    @property
    def nature(self) -> bool:
        """
        :return: True if the player is nature, False otherwise
        """
        return self is self.game.nature

    def __next__(self) -> Optional[P]:
        return None if self.nature else self.game.players[(self.index + 1) % len(self.game.players)]

    def __str__(self) -> str:
        return 'Nature' if self.nature else f'Player {self.index}'

    @property
    @abstractmethod
    def actions(self) -> List[Action[G, E, N, P]]:
        """
        :return: the actions of the player
        """
        pass

    @property
    @abstractmethod
    def payoff(self) -> int:
        """
        :return: the payoff of the player
        """
        pass

    @property
    def _private_information(self) -> Dict[str, Any]:
        return {
            **self._public_information,
            'actions': self.actions,
        }

    @property
    def _public_information(self) -> Dict[str, Any]:
        return {
            'actions': list(filter(lambda action: action.public, self.actions)),
        }
