from abc import ABC
from typing import Any, Optional, Sequence, TypeVar, Union, final

from gameframe.game import Action, E, Game, N, P
from gameframe.sequential.exceptions import ActorOutOfTurnException
from gameframe.utils import override

SG = TypeVar('SG', bound='SequentialGame')


class SequentialGame(Game[SG, E, N, P], ABC):
    """SequentialGame is the abstract base class for all sequential games.

    In sequential games, only one actor can act at a time.

    The actor in turn can be accessed through the actor property of the SequentialGame instance. The subclasses should
    define the actor who is the first to act. If a sequential game is terminal, its protected actor attribute must be
    set to None to denote such.
    """

    def __init__(self, environment: E, nature: N, players: Sequence[P], actor_index: Optional[int]) -> None:
        super().__init__(environment, nature, players)

        self._actor: Optional[Union[N, P]] = self.nature if actor_index is None else self.players[actor_index]

    @property
    @final
    def actor(self) -> Optional[Union[N, P]]:
        """
        :return: the actor in turn to act of the sequential game
        """
        return self._actor

    @property
    @final
    @override
    def terminal(self) -> bool:
        return self.actor is None

    @property
    @override
    def _information(self) -> dict[str, Any]:
        return {
            **super()._information,
            'actor': self.actor,
        }


class SequentialAction(Action[SG, E, N, P], ABC):
    """SequentialAction is the abstract base class for all sequential actions."""

    @override
    def _verify(self) -> None:
        super()._verify()

        if not isinstance(self.game, SequentialGame):
            raise TypeError('The game is not an instance of SequentialGame')
        if self.actor is not self.game.actor:
            raise ActorOutOfTurnException('The actor is not in turn to act')
