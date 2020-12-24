"""
This module defines utilities in gameservice.
"""


class Log:
    """
    This is a class that represents logs. Each log records information about an action taken in the game.
    """

    def __init__(self, action):
        self.__action_str = str(action)
        self.__player_str = str(action.player)

    def __str__(self):
        """
        Converts the log into a string representation.

        :return: the string representation of the log
        """
        return f'{self.__player_str}: {self.__action_str}'
