"""
name: message.py
description: message abstraction and messages types
subject: submarine game
creation date: 29/12/2020
"""
from packet.packet_operations import SubmarinePacket


class Message:
    """
    abstraction of message that can be sent over the protocol
    """

    def format_message(self) -> str:
        """
        formating a message object to a string that can be sent over protocol
        :return: string that represent the message
        """
        pass


class InitialConnectionMessage(Message):
    """
    abstraction of InitialConnection message that can be sent over the protocol
    """
    INIT_MESSAGE = 'HELLO'

    def format_message(self) -> str:
        return SubmarinePacket.struct_packet(InitialConnectionMessage.INIT_MESSAGE)


class InitialConnectionResponseMessage(Message):
    """
    abstraction of InitialConnectionResponse message that can be sent over the protocol
    """
    INIT_RESPONSE_MESSAGE = 'OLLEH'

    def format_message(self) -> str:
        """
        formating a InitialConnectionResponseMessage object to a string that can be sent over protocol
        :return: string that represent the InitialConnectionResponseMessage
        """
        return SubmarinePacket.struct_packet(InitialConnectionResponseMessage.INIT_RESPONSE_MESSAGE)


class BombMessage(Message):
    """
    abstraction of Bomb message that can be sent over the protocol
    """

    def __init__(self, x_coordinate, y_coordinate):
        self.x = x_coordinate
        self.y = y_coordinate
        self.message = f'BOMB~{self.x}~{self.y}'

    def format_message(self) -> str:
        """
        formating a BombMessage object to a string that can be sent over protocol
        :return: string that represent the BombMessage
        """
        return SubmarinePacket.struct_packet(self.message)


class MissMessage(Message):
    """
    abstraction of Miss message that can be sent over the protocol
    """
    MISS_MESSAGE = 'MISS'

    def format_message(self) -> str:
        """
        formating a MissMessage object to a string that can be sent over protocol
        :return: string that represent the MissMessage
        """
        return SubmarinePacket.struct_packet(MissMessage.MISS_MESSAGE)


class HitMessage(Message):
    """
    abstraction of Hit message that can be sent over the protocol
    """
    HIT_MESSAGE = 'HIT'

    def format_message(self) -> str:
        """
        formating a HitMessage object to a string that can be sent over protocol
        :return: string that represent the HitMessage
        """
        return SubmarinePacket.struct_packet(HitMessage.HIT_MESSAGE)


class SinkMessage(Message):
    """
    abstraction of Sink message that can be sent over the protocol
    """
    SINK_MESSAGE = 'SINK'

    def format_message(self) -> str:
        """
        formating a SinkMessage object to a string that can be sent over protocol
        :return: string that represent the SinkMessage
        """
        return SubmarinePacket.struct_packet(SinkMessage.SINK_MESSAGE)


class EndGameMessage(Message):
    """
    abstraction of End Game message that can be sent over the protocol
    """
    END_GAME_MESSAGE = 'GG'

    def format_message(self) -> str:
        """
        formating a EndGameMessage object to a string that can be sent over protocol
        :return: string that represent the EndGameMessage
        """
        return SubmarinePacket.struct_packet(EndGameMessage.END_GAME_MESSAGE)
