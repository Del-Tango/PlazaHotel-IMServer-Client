#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# IM CLIENT

import socket
import select
import string
import sys
import datetime
import logging
import pysnooper

log = logging.getLogger(__name__)


class PHChatClient():

    messages = {
        'register-alias': " ENTERING ORBIT:\n Register Alias: ",
        'connection-failed': " Can't connect to the server",
        'breaking-orbit': '\r' + ' ' * 80 + '\n\rBREAKING ORBIT!',
    }

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        self.alias = kwargs.get('alias')
        self.host = kwargs.get('host', '127.0.0.1')
        self.port = kwargs.get('port', 5041)
        self.room_buffer = kwargs.get('room_buffer', 4096)
        self.client_name = kwargs.get('client_name', 'PlazaHotel')
        self.room = kwargs.get('room', 13)
        self.floor = kwargs.get('floor', 'VIP')
        self.timestamp_format = kwargs.get('timestamp_format', '%d/%m/%Y %H:%M:%S')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # FORMATTERS

    def format_msg_breaking_orbit(self, message=messages['breaking-orbit']):
        log.debug('')
        return "\33[31m\33[1m" + message + "\33[0m"

    def format_msg_connection_failed(self, message=messages['connection-failed']):
        log.debug('')
        return "\33[31m\33[1m" + message + "\33[0m"

    def format_msg_register_alias(self, message=messages['register-alias']):
        log.debug('')
        return "\33[34m\33[1m" + message + "\33[0m"

    # DISPLAY

    def display(self):
        log.debug('')
        you = "\33[33m\33[1m \r" + self.alias + "> " + "\33[0m"
        sys.stdout.write(you)
        sys.stdout.flush()

    def display_server_banner(self):
        log.debug('')
        print(
            "\n\33[32m[ " + str(self.client_name) + " ]: "
            + datetime.datetime.now().strftime(self.timestamp_format)
            + " \33[0m\n"
        )

    # HANDLERS

    def handle_incomming_message(self, sock):
        log.debug('')
        data = sock.recv(self.room_buffer)
        if not data :
            print(self.format_msg_breaking_orbit())
            return False
        else:
            sys.stdout.write(data.decode())
            self.display()
            return True

#   @pysnooper.snoop('logs/plaza-hotel.log')
    def handle_outgoing_message(self):
        log.debug('')
        msg = sys.stdin.readline()
        self.server_socket.send(msg.encode())
        self.display()
        if msg.strip('\n') == '.exit':
            self.cleanup()
            print()
            sys.exit(0)

    # CLEANERS

    def cleanup(self):
        log.debug('')
        self.alias = ''

    # GENERAL

    def start_chatroom_client(self):
        log.debug('')
        while True:
            socket_list = [sys.stdin, self.server_socket]
            rList, wList, error_list = select.select(socket_list , [], [])
            for sock in rList:
                if sock == self.server_socket:
                    handle = self.handle_incomming_message(sock)
                    if not handle:
                        return
                else:
                    self.handle_outgoing_message()

    def connect_to_host(self, host, port):
        log.debug('')
        try :
            self.server_socket.connect((self.host, self.port))
            return True
        except :
            print(self.format_msg_connection_failed())
            return False

    # @pysnooper.snoop()
    def client_init(self):
        log.debug('')
#       self.display_server_banner()
        name = self.alias or input(self.format_msg_register_alias())
        self.alias = str(self.floor) + '/' + str(self.room) + '/' + name
        name = name.encode()
        self.server_socket.settimeout(2)
        connect = self.connect_to_host(self.host, self.port)
        if not connect:
            return False
        self.server_socket.send(name)
        self.display()
        try:
            self.start_chatroom_client()
        except Exception as e:
            self.cleanup()


if __name__ == "__main__":
    client = PHChatClient()
    client.client_init()
