"""
name: packet_operations.py
description: packet operations and structure of the given protocol
subject: submarine game
creation date: 29/12/2020
"""


class SubmarinePacket:
    """
    class for operation to create or the analyze Submarine packets.
    """
    MESSAGE_LENGTH_SIZE = 3
    LITTLE_ENDIAN = 'little'
    BIG_ENDIAN = 'big'

    @staticmethod
    def build_packet(message: str, length_endian_type: str) -> str:
        """
        build a packet structure with the message content and endian format for the message length
        :param message: the message content
        :param length_endian_type: the endian format the length of the message will be format
        :return: str that represent the concatenation of the message length and the message content
        """
        message_size = len(message)
        message_size_ascii = SubmarinePacket.convert_size_to_endian(message_size, length_endian_type)
        return message_size_ascii + message

    @staticmethod
    def convert_size_to_endian(message_size: int, endian_type: str) -> str:
        """
        convert length to ascii chars that represent the message size
        :param message_size: the length of the message content
        :param endian_type: type of endian we represent the message_size
        :return: the MESSAGE_LENGTH_SIZE size ascii string
        """
        message_size_bytes = message_size.to_bytes(SubmarinePacket.MESSAGE_LENGTH_SIZE, endian_type)
        message_size_ascii = [chr(byte) for byte in message_size_bytes]
        return ''.join(message_size_ascii)
