from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence, TYPE_CHECKING, Union, final

from gameframe.poker.actions import AggressiveAction, PassiveAction, SubmissiveAction
from gameframe.poker.utils import HoleCard
from gameframe.utils import override

if TYPE_CHECKING:
    from gameframe.poker import PokerAction, PokerGame, PokerNature, PokerPlayer


class Round(ABC):
    """Round is the abstract base class for all rounds."""

    def __init__(self, game: PokerGame) -> None:
        self.__game: PokerGame = game

    @property
    @final
    def game(self) -> PokerGame:
        """
        :return: the game of the round
        """
        return self.__game

    @property
    @abstractmethod
    def _opener(self) -> Union[PokerNature, PokerPlayer]:
        pass

    @abstractmethod
    def _open(self) -> None:
        pass

    @abstractmethod
    def _close(self) -> None:
        pass

    @abstractmethod
    def _create_actions(self) -> Sequence[PokerAction]:
        pass


@final
class BettingRound(Round, ABC):
    """BettingRound is the abstract base class for all betting rounds."""

    def __init__(self, game: PokerGame, board_card_count: int, hole_card_statuses: Sequence[bool]) -> None:
        super(BettingRound, self).__init__(game)

        self.__board_card_count: int = board_card_count
        self.__hole_card_statuses: Sequence[bool] = hole_card_statuses

    @property
    @override
    def _opener(self) -> Union[PokerNature, PokerPlayer]:
        if any(player.bet for player in self.game.players):
            opener: PokerPlayer = min(self.game.players, key=lambda player: (player.bet, player.index))

            return opener if opener._relevant else next(opener)
        else:
            try:
                return next(player for player in self.game.players if player._relevant)
            except StopIteration:
                return self.game.nature

    @override
    def _open(self) -> None:
        self.game.environment.board_cards.extend(self.game._deck.draw(self.__board_card_count))

        for player in self.game.players:
            if not player._mucked:
                for hole_card, status in zip(self.game._deck.draw(len(self.__hole_card_statuses)),
                                             self.__hole_card_statuses):
                    player.hole_cards.append(HoleCard(hole_card, status))

        if not self._opener.nature:
            self.game.environment._aggressor = self.game.actor
            self.game.environment._max_delta = max(self.game._blinds)

    @override
    def _close(self) -> None:
        self.game.environment._max_delta = None
        self.game.environment._pot += sum(player.bet for player in self.game.players)

        for player in self.game.players:
            player._bet = 0

    @override
    def _create_actions(self) -> Sequence[PokerAction]:
        actions: list[PokerAction] = []

        if self.game.actor.bet < max(player.bet for player in self.game.players):
            actions.append(SubmissiveAction(self.game.actor))

        actions.append(PassiveAction(self.game.actor))

        if sum(player._relevant for player in self.game.players) > 1 and \
                max(player.bet for player in self.game.players) < self.game.actor.stack:
            if self.game._lazy:
                bet_amounts: Sequence[int] = list({self.game._limit.min_amount, self.game._limit.max_amount})
            else:
                bet_amounts: Sequence[int] = range(self.game._limit.min_amount, self.game._limit.max_amount + 1)

            actions.extend(map(lambda amount: AggressiveAction(self.game.actor, amount), bet_amounts))

        return actions
