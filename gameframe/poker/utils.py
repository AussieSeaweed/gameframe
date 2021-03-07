import re
from collections.abc import Iterable

from pokertools import parse_cards

from gameframe.poker.bases import PokerGame, PokerPlayer


def parse_poker(game: PokerGame, tokens: Iterable[str]) -> None:
    """Parses the tokens as actions and applies them the supplied poker game.

    :param game: The poker game to be applied on.
    :param tokens: The tokens to parse as actions.
    :return: None.
    """
    for token in tokens:
        if isinstance(game._actor, PokerPlayer):
            if match := re.fullmatch(r'br (?P<amount>\d+)', token):
                game._actor.bet_raise(int(match.group('amount')))
            elif token == 'cc':
                game._actor.check_call()
            elif token == 'f':
                game._actor.fold()
            elif match := re.fullmatch(r's( (?P<force>[0|1]))?', token):
                game._actor.showdown(False if match.group('force') is None else bool(match.group('force')))
            else:
                raise ValueError('Invalid command')
        else:
            if match := re.fullmatch(r'dh (?P<index>\d+) (?P<cards>\w+)', token):
                game.nature.deal_hole(game.players[int(match.group('index'))], parse_cards(match.group('cards')))
            elif match := re.fullmatch(r'db (?P<cards>\w+)', token):
                game.nature.deal_board(parse_cards(match.group('cards')))
            else:
                raise ValueError('Invalid command')
