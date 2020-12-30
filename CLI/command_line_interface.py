"""
name: command_line_interface.py
description: command line interface for running a game against other player
subject: submarine game
creation date: 29/12/2020
"""
import socket
from messages.message import InitialConnectionMessage, InitialConnectionResponseMessage, BombMessage, MissMessage, \
    HitMessage, SinkMessage, EndGameMessage
from packet.packet_operations import SubmarinePacket


class CommandLineInterface:
    """
    Command line interface for using the submarine game protocol
    """
    GAME_PORT = 8765
    MESSAGE_LENGTH_SIZE = 3
    MISS_MESSAGE_DATA = 'MISS'
    EMPTY_STRING = ''

    def start_game(self):
        """
        Function for start the game loop between 2 players
        :return: None
        """
        pass

    @staticmethod
    def read_message(socket_to_read_from):
        """
        Static method for reading protocol data from sockets
        :param socket_to_read_from: the socket which the data sent to
        :return: the data received from socket
        """
        message_received_length = socket_to_read_from.recv(CommandLineInterface.MESSAGE_LENGTH_SIZE).decode('ascii')
        if message_received_length != CommandLineInterface.EMPTY_STRING:
            message_received_data = socket_to_read_from.recv(
                SubmarinePacket.get_received_packet_size(message_received_length))
            print(message_received_data.decode('ascii'))
            return message_received_data.decode('ascii')
        else:
            socket_to_read_from.close()
            print('Other player disconnected')
            exit(0)


class HostCommandLineInterface(CommandLineInterface):
    """
    Command line interface for a player that chose to host the game
    """

    def __init__(self):
        """
        Initial actions dictionary and game socket which the host will listen with
        """
        self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.str_to_action = {'init': self.send_init_game,
                              'bomb': self.send_bomb,
                              'hit': self.send_hit,
                              'miss': self.send_miss,
                              'sink': self.send_sink,
                              'end': self.send_end_game,
                              'exit': self.exit_game}
        self.client_socket = None

    def start_game(self):
        """
        Host function to start game loop with other player
        :return: None
        """
        self.game_socket.bind((self.EMPTY_STRING, self.GAME_PORT))
        self.game_socket.listen()
        print('wait for connections...')
        (other_player_socket, other_player_address) = self.game_socket.accept()
        self.client_socket = other_player_socket
        print('Got connection from', other_player_address)
        while True:
            execution_command = self.execute_action()
            if execution_command == self.MISS_MESSAGE_DATA.lower():
                continue
            received_data = self.read_message(other_player_socket)
            while received_data == self.MISS_MESSAGE_DATA:
                received_data = self.read_message(other_player_socket)

    def execute_action(self):
        """
        Reading from user a game action and validating its an action from possible actions
        :return: the chosen action selected
        """
        print('---------------------------------')
        for action_name, _ in self.str_to_action.items():
            print(action_name)
        user_input = input('Enter command to execute from the above:')
        print('---------------------------------')
        while user_input not in self.str_to_action.keys():
            user_input = input('Not valid action!\nEnter command to execute from the above:')
        self.str_to_action[user_input]()
        return user_input

    def send(self, message_to_send):
        """
        Send message to the other player we playing with
        :param message_to_send: the message we want to send
        :return: None
        """
        try:
            self.client_socket.send(message_to_send.encode('ascii'))
        except OSError:
            print('not connected to other player socket...')
            exit(0)

    def send_init_game(self):
        """
        Send initial message for the other player by the protocol
        :return:None
        """
        init_game_message = InitialConnectionMessage()
        self.send(init_game_message.format_message())

    def send_bomb(self):
        """
        Send bomb message for the other player by the protocol
        :return: None
        """
        x_coordinate = input('Enter x: ')
        while not x_coordinate.isnumeric():
            x_coordinate = input('Enter numeric x: ')
        y_coordinate = input('Enter y: ')
        while not y_coordinate.isnumeric():
            y_coordinate = input('Enter numeric y: ')
        bomb_message = BombMessage(int(x_coordinate), int(y_coordinate))
        print('---------------------------------')
        self.send(bomb_message.format_message())

    def send_miss(self):
        """
        Send miss message for the other player by the protocol
        :return: None
        """
        miss_message = MissMessage()
        self.send(miss_message.format_message())

    def send_hit(self):
        """
        Send hit message for the other player by the protocol
        :return: None
        """
        hit_message = HitMessage()
        self.send(hit_message.format_message())

    def send_sink(self):
        """
        Send sink message for the other player by the protocol
        :return: None
        """
        sink_message = SinkMessage()
        self.send(sink_message.format_message())

    def send_end_game(self):
        """
        Send end game message for the other player by the protocol
        :return: None
        """
        end_game_message = EndGameMessage()
        self.send(end_game_message.format_message())

    def exit_game(self):
        """
        End the connection and exit the program
        :return:None
        """
        self.game_socket.close()
        print('Bye bye')
        exit(0)


class ClientCommandLineInterface(CommandLineInterface):
    """
    Command line interface for a player that connect to host that wait for game initialization
    """

    def __init__(self, host_ip: str):
        """
        Initial actions dictionary and game socket which the client will use to connect with the host
        :param host_ip: the host IP we want to connect to
        """
        self.game_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.str_to_action = {'init': self.send_init_game,
                              'bomb': self.send_bomb,
                              'hit': self.send_hit,
                              'miss': self.send_miss,
                              'sink': self.send_sink,
                              'end': self.send_end_game,
                              'exit': self.exit_game}
        self.host_address = (host_ip, self.GAME_PORT)

    def start_game(self):
        """
        Client function to start game loop with other player
        :return: None
        """
        print(f'try to connect to other player...')
        try:
            self.game_socket.connect(self.host_address)
        except OSError:
            print('Could not connect to other player...')
            exit(0)
        print('Connected!')
        while True:
            received_data = self.read_message(self.game_socket)
            while received_data == self.MISS_MESSAGE_DATA:
                received_data = self.read_message(self.game_socket)
            execution_command = self.execute_action()
            while execution_command == self.MISS_MESSAGE_DATA.lower():
                execution_command = self.execute_action()

    def execute_action(self):
        """
        Reading from user a game action and validating its an action from possible actions
        :return: the chosen action selected
        """
        print('---------------------------------')
        for action_name, _ in self.str_to_action.items():
            print(action_name)
        user_input = input('Enter command to execute from the above:')
        print('---------------------------------')
        while user_input not in self.str_to_action.keys():
            user_input = input('Not valid action!\nEnter command to execute from the above:')
        self.str_to_action[user_input]()
        return user_input

    def send(self, message_to_send):
        """
        Send message to the other player we playing with
        :param message_to_send: the message we want to send
        :return: None
        """
        try:
            self.game_socket.sendto(message_to_send.encode('ascii'), self.host_address)
        except OSError:
            print('not connected to other player socket...')
            exit(0)

    def send_init_game(self):
        """
        Send initial message for the other player by the protocol
        :return:None
        """
        init_res_game_message = InitialConnectionResponseMessage()
        self.send(init_res_game_message.format_message())

    def send_bomb(self):
        """
        Send bomb message for the other player by the protocol
        :return: None
        """
        x_coordinate = input('Enter x: ')
        while not x_coordinate.isnumeric():
            x_coordinate = input('Enter numeric x: ')
        y_coordinate = input('Enter y: ')
        while not y_coordinate.isnumeric():
            y_coordinate = input('Enter numeric y: ')
        bomb_message = BombMessage(int(x_coordinate), int(y_coordinate))
        print('---------------------------------')
        self.send(bomb_message.format_message())

    def send_miss(self):
        """
        Send miss message for the other player by the protocol
        :return: None
        """
        miss_message = MissMessage()
        self.send(miss_message.format_message())

    def send_hit(self):
        """
        Send hit message for the other player by the protocol
        :return: None
        """
        hit_message = HitMessage()
        self.send(hit_message.format_message())

    def send_sink(self):
        """
        Send sink message for the other player by the protocol
        :return: None
        """
        sink_message = SinkMessage()
        self.send(sink_message.format_message())

    def send_end_game(self):
        """
        Send end game message for the other player by the protocol
        :return: None
        """
        end_game_message = EndGameMessage()
        self.send(end_game_message.format_message())

    def exit_game(self):
        """
        End the connection and exit the program
        :return:None
        """
        self.game_socket.close()
        print('Bye bye')
        exit(0)
