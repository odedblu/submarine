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

    @staticmethod
    def struct_packet(message: str) -> str:
        """
        build a packet structure with the message content and endian format for the message length
        :param message: the message content
        :return: str that represent the concatenation of the message length and the message content
        """
        return SubmarinePacket.get_packet_size_three_chars(len(message)) + message

    @staticmethod
    def get_packet_size_three_chars(message_size: int) -> str:
        """
        gett the message size string to append to message
        :param message_size: the message data size
        :return: string of length MESSAGE_LENGTH_SIZE that represents the data size
        """
        if message_size > 999:
            return '999'
        result = str(message_size)
        while len(result) != SubmarinePacket.MESSAGE_LENGTH_SIZE:
            result = f'0{result}'
        return result

    @staticmethod
    def get_received_packet_size(received_packet_size: str) -> int:
        """
        convert the MESSAGE_LENGTH_SIZE first chars to integer
        :param received_packet_size: the MESSAGE_LENGTH_SIZE first chars of received packet
        :return: the length of the packet data
        """
        return int(received_packet_size)
