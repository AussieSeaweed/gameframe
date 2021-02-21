from collections import Sequence
from typing import Optional, cast
from unittest import TestCase, main

from pokertools import parse_card, parse_cards

from gameframe.game import ActionException
from gameframe.poker import NLSGame, NLTGame, PLOGame, PokerGame, PokerPlayer, parse_poker_game
from gameframe.poker._stages import ShowdownStage


class NLTSimTestCase(TestCase):
    ANTE = 1
    BLINDS = 1, 2

    def test_not_betting_stage(self) -> None:
        self.assertRaises(ActionException, self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                                                      'cc cc cc cb2c', False).players[1].fold)
        self.assertRaises(ActionException, self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                                                      'cc cc cc cc', False).players[0].check_call)
        self.assertRaises(ActionException, self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                                                      'cc cc cc cb2b4c', False).players[0].bet_raise, 100)
        self.assertRaises(ActionException, self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                                                      ['AcAsKc', 'Qs', 'Qc'],
                                                      'cccc cccc cccc cccb2ccc').players[0].fold)
        self.assertRaises(ActionException, self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                                                      ['AcAsKc', 'Qs', 'Qc'],
                                                      'cccc cccc cccc cccc').players[0].check_call)
        self.assertRaises(ActionException, self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                                                      ['AcAsKc', 'Qs', 'Qc'],
                                                      'cccc cccc cccc cccb2b4b6ccc').players[1].bet_raise, 8)

    def test_redundant_fold(self) -> None:
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'cf')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'cc f')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs'], 'cb4c cc f')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                          'cb4c cc cc f')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], [],
                          'cccf')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc'], 'b6ffc f')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs'], 'cccc cccc cccf')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs', 'Qc'], 'ffcc cc cc cf')

    def test_covered_stack(self) -> None:
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'b6b199b100')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b6c cb50b193b93')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs'],
                          'cb4c cc b195b95')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                          'b6c cc cc b93b93')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], [],
                          'b299ccb99')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc'], 'ffcc b197b50')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs'], 'cccc cccc b197ccb197')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs', 'Qc'], 'b6ccc cccc cccc ccb293b193')

    def test_redundant_bet_raise(self) -> None:
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'b99b197')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b6c cb93b193')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs'],
                          'cb4c cc cb95b195')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                          'b6c cc cc cb93b193')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], [],
                          'cccb99cb199cb199')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc'], 'fb6fc b93b193')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs'], 'cfcc ccc b197cb297')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs', 'Qc'], 'cffc b10c b10b20c b67b267')

    def test_bet_amount(self) -> None:
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], [], 'b6b9')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b6c b12b24b30')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs'],
                          'cb4c b4c b4b8b10')
        self.assertRaises(ActionException, self.parse, [200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'],
                          'b6c cc cc b1')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], [],
                          'ccb98b99b100')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc'], 'cccc b2b4b6b8ccb9')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs'], 'cccc cccc b96b97b98')
        self.assertRaises(ActionException, self.parse, [200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'],
                          ['AcAsKc', 'Qs', 'Qc'], 'ffcc cc cc b50b55')

    def test_aggressor(self) -> None:
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6b99c', False), 0)
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b99c', False), 1)
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cc cc cc cc', False), 0)
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cc cc cb6c cc', False), 0)
        self.assert_actor(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cc cc cc cb6b12c', False),
                          0)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b299ccc', False), 2)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'ffb99c', False), 0)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'cccc cccc cccc cccc', False), 0)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'cccc cccc cb2ccc cccc', False), 0)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'cccc cccc cccc b6b12b297ccc', False), 2)
        self.assert_actor(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'fb199cc', False), 0)
        self.assert_actor(self.parse([100] * 4, ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b99ccc', False), 0)

    def test_showdown(self) -> None:
        self.assert_shows(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6b199c'), [True, True])
        self.assert_shows(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b99c'), [False, True])
        self.assert_shows(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6c cc cc cc'),
                          [True, True])
        self.assert_shows(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cc cc cc cc'), [True, True])
        self.assert_shows(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b4c b6f'), [False, False])
        self.assert_shows(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b299ccc'), [True, True, True, False])
        self.assert_shows(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'fb6cc ccc ccc ccc'), [True, True, False, False])
        self.assert_shows(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'fb6cc ccb10b20cf cc cb50c'), [False, True, False, False])
        self.assert_shows(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b6ccc ccb10b20cb93ccc ccc ccc'), [True, True, False, False])
        self.assert_shows(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'b6ccc ccb10b20cb93ccc b50cc ccc'), [True, True, False, False])
        self.assert_shows(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                     'fb199cc'), [True, True, False, False])
        self.assert_shows(self.parse([100] * 4, ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], 'b99ccc'),
                          [True, True, False, False])
        self.assert_shows(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'JcJh', 'TsTh'],
                                     ['AcAsKc', 'Qs', 'Qc'], 'cccb149ccccc cccc cccc cccc'),
                          [True, True, False, False, False, False])
        self.assert_shows(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'JcJh', 'TsTh'],
                                     [], 'b50fffff'), [False, False, False, False, False, False])
        self.assert_shows(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'TsTh', 'JcTc'],
                                     ['AcAsKc', 'Qs', 'Qc'], 'b50b199ccccf'), [True, True, False, False, False, True])

        self.assert_shows(self.parse([0, 0], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [True, True])
        self.assert_shows(self.parse([1, 0], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [True, True])
        self.assert_shows(self.parse([0, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [True, True])
        self.assert_shows(self.parse([2, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [True, True])
        self.assert_shows(self.parse([50, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [True, True])
        self.assert_shows(self.parse([0, 0, 0, 0], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], ''),
                          [True, True, False, False])
        self.assert_shows(self.parse([1, 1, 5, 5], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], 'b4c'),
                          [True, True, True, False])
        self.assert_shows(self.parse([7, 0, 9, 7], ['4h8s', 'AsQs', 'Ac8d', 'AhQh'], ['Ad3s2h', '8h', 'Ts'], 'ff'),
                          [True, True, False, False])
        self.assert_shows(self.parse([1, 17, 0, 1], ['3d6c', '8sAh', 'Ad8c', 'KcQs'], ['4c7h5s', 'Ts', '3c'], ''),
                          [True, True, True, False])
        self.assert_shows(self.parse([2, 16, 0, 1], ['AcKs', '8h2c', '6h6c', '2dTd'], ['8d5c4d', 'Qh', '5d'], ''),
                          [False, True, False, True])

    def test_distribution(self) -> None:
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6b199c'), [100, 200])
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b99c'), [100, 200])
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'b6c cc cc cc'), [193, 107])
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], 'cc cc cc cc'), [197, 103])
        self.assert_stacks(self.parse([200, 100], ['QdQh', 'AhAd'], ['AcAsKc'], 'b4cb6f'), [205, 95])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'b299ccc'), [300, 400, 100, 0])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'fb6cc ccc ccc ccc'), [193, 115, 299, 193])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'fb6cc ccb10b20cf cc cb50c'), [123, 195, 299, 183])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'b6ccc ccb10b20cb93ccc ccc ccc'), [100, 400, 200, 100])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'b6ccc ccb10b20cb93ccc b50cc ccc'), [200, 400, 150, 50])
        self.assert_stacks(self.parse([200, 100, 300, 200], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'],
                                      'fb199cc'), [200, 301, 299, 0])
        self.assert_stacks(self.parse([100] * 4, ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], 'b99ccc'),
                           [0, 400, 0, 0])
        self.assert_stacks(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'JcJh', 'TsTh'],
                                      ['AcAsKc', 'Qs', 'Qc'], 'cccb149ccccc cccc cccc cccc'),
                           [300, 600, 150, 50, 50, 0])
        self.assert_stacks(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'JcJh', 'TsTh'],
                                      [], 'b50fffff'), [198, 97, 308, 199, 199, 149])
        self.assert_stacks(self.parse([200, 100, 300, 200, 200, 150], ['QdQh', 'AhAd', 'KsKh', 'JsJd', 'TsTh', 'JcTc'],
                                      ['AcAsKc', 'Qs', 'Qc'], 'b50b199ccccf'), [150, 0, 249, 0, 0, 751])

        self.assert_stacks(self.parse([0, 0], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [0, 0])
        self.assert_stacks(self.parse([1, 0], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [1, 0])
        self.assert_stacks(self.parse([0, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [0, 1])
        self.assert_stacks(self.parse([2, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [1, 2])
        self.assert_stacks(self.parse([50, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], ''), [49, 2])
        self.assert_stacks(self.parse([0, 0, 0, 0], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], ''),
                           [0, 0, 0, 0])
        self.assert_stacks(self.parse([1, 1, 5, 5], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], 'b4c'),
                           [0, 4, 8, 0])
        self.assert_stacks(self.parse([7, 0, 9, 7], ['4h8s', 'AsQs', 'Ac8d', 'AhQh'], ['Ad3s2h', '8h', 'Ts'], 'ff'),
                           [9, 0, 8, 6])
        self.assert_stacks(self.parse([1, 17, 0, 1], ['3d6c', '8sAh', 'Ad8c', 'KcQs'], ['4c7h5s', 'Ts', '3c'], ''),
                           [3, 16, 0, 0])
        self.assert_stacks(self.parse([2, 16, 0, 1], ['AcKs', '8h2c', '6h6c', '2dTd'], ['8d5c4d', 'Qh', '5d'], ''),
                           [0, 16, 0, 3])

    def test_pot(self) -> None:
        self.assertEqual(self.parse([0, 0], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], '').pot, 0)
        self.assertEqual(self.parse([1, 0], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], '').pot, 0)
        self.assertEqual(self.parse([0, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], '').pot, 0)
        self.assertEqual(self.parse([2, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], '').pot, 0)
        self.assertEqual(self.parse([50, 1], ['QdQh', 'AhAd'], ['AcAsKc', 'Qs', 'Qc'], '').pot, 0)
        self.assertEqual(self.parse([0, 0, 0, 0], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], '').pot, 0)
        self.assertEqual(self.parse([1, 1, 5, 5], ['QdQh', 'AhAd', 'KsKh', 'JsJd'], ['AcAsKc', 'Qs', 'Qc'], 'b4c').pot,
                         0)
        self.assertEqual(self.parse([7, 0, 9, 7], ['4h8s', 'AsQs', 'Ac8d', 'AhQh'], ['Ad3s2h', '8h', 'Ts'], 'ff').pot,
                         0)
        self.assertEqual(self.parse([1, 17, 0, 1], ['3d6c', '8sAh', 'Ad8c', 'KcQs'], ['4c7h5s', 'Ts', '3c'], '').pot, 0)
        self.assertEqual(self.parse([2, 16, 0, 1], ['AcKs', '8h2c', '6h6c', '2dTd'], ['8d5c4d', 'Qh', '5d'], '').pot, 0)
        self.assertEqual(self.parse([2, 16, 0, 1], ['AcKs', '8h2c', '6h6c', '2dTd'], ['8d5c4d', 'Qh', '5d'], '').pot, 0)

    def test_nlt_cans(self) -> None:
        game = NLTGame(1, [1, 2], [100, 100, 100])
        n = game.nature
        a, b, c = game.players

        self.assertTrue(n.can_deal_player())
        self.assertTrue(n.can_deal_player(a))
        self.assertTrue(n.can_deal_player(b))
        self.assertTrue(n.can_deal_player(c))
        self.assertFalse(n.can_deal_board())
        self.assertEqual(n.player_deal_count, 2)

        n.deal_player(a, parse_card('Ah'), parse_card('Th'))

        self.assertTrue(n.can_deal_player())
        self.assertFalse(n.can_deal_player(a))
        self.assertTrue(n.can_deal_player(b))
        self.assertTrue(n.can_deal_player(c))
        self.assertFalse(n.can_deal_board())
        self.assertEqual(n.player_deal_count, 2)

        n.deal_player(b, parse_card('As'), parse_card('Ts'))
        n.deal_player(c, parse_card('Ac'), parse_card('Tc'))

        self.assertFalse(n.can_deal_player())
        self.assertFalse(n.can_deal_board())

        self.assertFalse(a.can_fold())
        self.assertFalse(a.can_bet_raise())
        self.assertFalse(a.can_check_call())
        self.assertFalse(b.can_fold())
        self.assertFalse(b.can_bet_raise())
        self.assertFalse(b.can_check_call())
        self.assertTrue(c.can_fold())
        self.assertTrue(c.can_bet_raise())
        self.assertTrue(c.can_check_call())
        self.assertTrue(c.can_bet_raise(4))
        self.assertTrue(c.can_bet_raise(99))
        self.assertFalse(c.can_bet_raise(0))
        self.assertEqual(c.min_bet_raise_amount, 4)
        self.assertEqual(c.max_bet_raise_amount, 99)

        c.bet_raise(6)

        self.assertTrue(a.can_fold())
        self.assertTrue(a.can_bet_raise())
        self.assertTrue(a.can_check_call())
        self.assertFalse(b.can_fold())
        self.assertFalse(b.can_bet_raise())
        self.assertFalse(b.can_check_call())
        self.assertFalse(c.can_fold())
        self.assertFalse(c.can_bet_raise())
        self.assertFalse(c.can_check_call())
        self.assertEqual(a.min_bet_raise_amount, 10)
        self.assertEqual(a.max_bet_raise_amount, 99)

        a.fold()
        b.check_call()

        self.assertFalse(n.can_deal_player())
        self.assertFalse(n.can_deal_player(a))
        self.assertFalse(n.can_deal_player(b))
        self.assertFalse(n.can_deal_player(c))
        self.assertTrue(n.can_deal_board())
        self.assertEqual(n.board_deal_count, 3)
        n.deal_board(*parse_cards('2h3h4h'))

        b.check_call()
        c.check_call()

        self.assertEqual(n.board_deal_count, 1)
        n.deal_board(parse_card('4s'))

        b.bet_raise(93)
        c.check_call()

        self.assertEqual(n.board_deal_count, 1)
        n.deal_board(parse_card('5s'))

        self.assertTrue(b.can_showdown())
        self.assertFalse(c.can_showdown())

        b.showdown()
        c.showdown()

        self.assertTrue(game.terminal)

    def assert_actor(self, game: PokerGame, index: Optional[int]) -> None:
        if isinstance(game.actor, PokerPlayer):
            self.assertEqual(game.actor.index, index)
        else:
            self.assertIsNone(index)

    def assert_shows(self, game: PokerGame, shows: Sequence[bool]) -> None:
        self.assertSequenceEqual([player.shown for player in game.players], shows)

    def assert_stacks(self, game: PokerGame, stacks: Sequence[int]) -> None:
        self.assertSequenceEqual([player.stack for player in game.players], stacks)

    def parse(self, stacks: Sequence[int], hole_card_sets: Sequence[str], board_card_sets: Sequence[str], tokens: str,
              terminate: bool = True) -> NLTGame:
        tokens = tokens.replace(' ', '')
        game = NLTGame(self.ANTE, self.BLINDS, stacks)

        for player, hole_cards in zip(game.players, hole_card_sets):
            game.nature.deal_player(player, *parse_cards(hole_cards))

        try:
            while tokens or board_card_sets:
                if isinstance(game.actor, PokerPlayer):
                    token, tokens = tokens[0], tokens[1:]

                    if token == 'b':
                        index = len(tokens) if tokens.isdigit() else next(
                            i for i, c in enumerate(tokens) if not c.isdigit())

                        amount, tokens = int(tokens[:index]), tokens[index:]
                        game.actor.bet_raise(amount)
                    elif token == 'c':
                        game.actor.check_call()
                    elif token == 'f':
                        game.actor.fold()
                    else:
                        self.fail()
                else:
                    game.nature.deal_board(*parse_cards(board_card_sets[0]))
                    board_card_sets = board_card_sets[1:]
        except ActionException as exception:
            assert not tokens and not board_card_sets, 'DEBUG: An exception was raised before all commands were parsed'
            raise exception

        while terminate and not game.terminal and isinstance(game._stage, ShowdownStage):
            cast(PokerPlayer, game.actor).showdown()

        return game


class PLOSimTestCase(TestCase):
    def test_amount(self) -> None:
        game = PLOGame(0, [1, 2], [100, 100])

        game.nature.deal_player(game.players[0], *parse_cards('AhAsKhKs'))
        game.nature.deal_player(game.players[1], *parse_cards('AcAdKcKd'))

        self.assertEqual(game.players[1].max_bet_raise_amount, 6)

        game = PLOGame(0, [1, 2], [100, 100, 100])

        game.nature.deal_player(game.players[0], *parse_cards('AhAsKhKs'))
        game.nature.deal_player(game.players[1], *parse_cards('AcAdKcKd'))
        game.nature.deal_player(game.players[2], *parse_cards('QcQdJcJd'))

        self.assertEqual(game.players[2].max_bet_raise_amount, 7)

        game.players[2].bet_raise(7)

        self.assertEqual(game.players[0].max_bet_raise_amount, 23)

        game = PLOGame(1, [1, 2], [100, 100])

        game.nature.deal_player(game.players[0], *parse_cards('AhAsKhKs'))
        game.nature.deal_player(game.players[1], *parse_cards('AcAdKcKd'))

        self.assertEqual(game.players[1].max_bet_raise_amount, 8)


class NLSSimTestCase(TestCase):
    def test_pre_flop(self) -> None:
        game = NLSGame(3000, 3000, [495000, 232000, 362000, 403000, 301000, 204000])

        parse_poker_game(
            game,
            'dp 0 Th8h', 'dp 1 QsJd', 'dp 2 QhQd', 'dp 3 8d7c', 'dp 4 KhKs', 'dp 5 8c7h',
            'cc', 'cc', 'cc', 'cc', 'cc', 'cc',
        )

        self.assertIs(game.actor, game.nature)

        game = NLSGame(3000, 3000, [495000, 232000, 362000, 403000, 301000, 204000])

        parse_poker_game(
            game,
            'dp 0 Th8h', 'dp 1 QsJd', 'dp 2 QhQd', 'dp 3 8d7c', 'dp 4 KhKs', 'dp 5 8c7h',
            'cc', 'cc', 'cc', 'cc', 'cc', 'br 35000', 'cc', 'cc', 'cc', 'cc', 'cc',
        )

        self.assertIs(game.actor, game.nature)


if __name__ == '__main__':
    main()
