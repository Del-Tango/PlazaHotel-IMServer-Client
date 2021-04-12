#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# IM SERVER

import socket
import select
import datetime
import pysnooper
import threading
import logging

log = logging.getLogger(__name__)


class PHChatServer():

    messages = {
        'username-taken': "Username already taken!",
        'welcome': "Welcome to room (--room--) on floor (--floor--), --client-count--/--capacity-- orbitals online. Type '--terminate-key--' to break orbit.\n",
        'client-connected': "--timestamp-- - Client <--client-address-->, --client-alias-- orbit entry!",
        'client-offline': "--timestamp-- - Client <--client-details-->, --client-alias-- breaking orbit!",
        'client-joined': "--client-alias--: ORBIT ENTRY! --client-count--/--capacity-- orbitals online.",
        'client-left': "--client-details--: BREAKING ORBIT! --client-count--/--capacity-- orbitals online.",
        'client-left-unexpectedly': "--client-alias-- broke orbit unexpectedly!",
        'client-message': "--client-alias--: --client-data--",
        'client-offline-error': "--timestamp-- [ ERROR ]: Client (<--client-details-->, --client-alias--) is offline!",
    }

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        self.room_buffer = kwargs.get('room_buffer', 4096) # buffer size in bytes
        self.server_name = kwargs.get('server_name', 'PlazaHotel')
        self.address = kwargs.get('address', '127.0.0.1')
        self.port = kwargs.get('port', 5041)
        self.floor = kwargs.get('floor', 'VIP')
        self.room = kwargs.get('room', 13)
        # [ NOTE ]: Listen atmost 10 connection at one time.
        self.capacity = kwargs.get('capacity', 10)
        self.terminate_key = kwargs.get('terminate_key', '.exit')
        self.timestamp_format = kwargs.get('timestamp_format', '%d/%m/%Y-%H:%M:%S')
        self.name = ""
        self.silent = kwargs.get('silent', 'on')   # (on | off)
        # [ NOTE ]: Dictionary to store address corresponding to username
        self.record = {}
        # [ NOTE ]: List to keep track of socket descriptors
        self.connected_list = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # GENERAL

    def refresh_im_server_values(self):
        log.debug('')
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.record = {}
        self.connected_list = []
        return True

    #@pysnooper.snoop()
    def send_to_all(self, sock, message):
        log.debug('')
        for socket in self.connected_list:
            if socket != self.server_socket and socket != sock :
                try:
                    socket.send(message.encode())
                except:
                    socket.close()
                    self.connected_list.remove(socket)

    # DISPLAY

    def display_server_banner(self):
        log.debug('')
        banner = "\n\33[32m[ " + str(self.server_name) + " ]: Room ("\
            + str(self.room) + ") on floor (" + str(self.floor)\
            + "), port number (" + str(self.port) + ")\33[0m"
        if not self.silent:
            print(banner)
        log.info(banner)
        return True

    # FORMATTERS

    def format_msg_client_offline_error(self, client_details, client_alias,
                                        message=messages['client-offline-error']):
        log.debug('')
        formatted_msg = message[:]
        formatted_msg = formatted_msg.replace(
            '--timestamp--', str(
                datetime.datetime.now().strftime(self.timestamp_format)
            )
        )
        formatted_msg = formatted_msg.replace(
            '--client-details--', str(client_details)
        )
        formatted_msg = formatted_msg.replace(
            '--client-alias--', str(client_alias)
        )
        return str(formatted_msg)

    def format_msg_client_left_unexpectedly(self, client_alias,
                                            message=messages['client-left-unexpectedly']):
        log.debug('')
        formatted_msg = message[:]
        formatted_msg = formatted_msg.replace(
            '--client-alias--', str(client_alias)
        )
        return "\r\33[31m \33[1m" + str(formatted_msg) + "\33[0m\n"

#   @pysnooper.snoop()
    def format_msg_client_message(self, client_alias, client_data,
                                message=messages['client-message']):
        log.debug('')
        formatted_msg = message[:]
        formatted_msg = formatted_msg.replace(
            '--client-alias--', "\r\33[1m" + "\33[35m " + str(client_alias)
        )
        formatted_msg = formatted_msg.replace(
            '--client-data--', "\33[0m" + str(client_data)
        )
        padding = 0 if len(formatted_msg) >= 80 else 80 - len(formatted_msg)
        formatted_msg += ' ' * padding
        formatted_msg += '\n'
        return str(formatted_msg)

    def format_msg_username_taken(self, message=messages['username-taken']):
        log.debug('')
        return "\r\33[31m\33[1m " + str(message) + "\n\33[0m"

    def format_msg_client_connected(self, client_addr, client_alias,
                                    message=messages['client-connected']):
        log.debug('')
        formatted_msg = message[:]
        formatted_msg = formatted_msg.replace(
            '--timestamp--', str(
                datetime.datetime.now().strftime(self.timestamp_format)
            )
        )
        formatted_msg = formatted_msg.replace(
            '--client-address--', str(client_addr)
        )
        formatted_msg = formatted_msg.replace(
            '--client-alias--', str(client_alias)
        )
        return str(formatted_msg)

    def format_msg_welcome(self, term=None, message=messages['welcome']):
        log.debug('')
        formatted_msg = message[:]
        term = term or self.terminate_key
        formatted_msg = formatted_msg.replace('--room--', str(self.room))
        formatted_msg = formatted_msg.replace('--floor--', str(self.floor))
        formatted_msg = formatted_msg.replace(
            '--client-count--', str(len(self.connected_list) - 1)
        )
        formatted_msg = formatted_msg.replace(
            '--capacity--', str(self.capacity)
        )
        formatted_msg = formatted_msg.replace('--terminate-key--', str(term))
        return "\33[32m\r\33[1m " + str(formatted_msg) + "\n\33[0m"

    def format_msg_client_joined(self, client_alias,
                                 message=messages['client-joined']):
        log.debug('')
        formatted_msg = message[:]
        formatted_msg = formatted_msg.replace(
            '--client-alias--', str(client_alias)
        )
        formatted_msg = formatted_msg.replace(
            '--client-count--', str(len(self.connected_list) - 1)
        )
        formatted_msg = formatted_msg.replace(
            '--capacity--', str(self.capacity)
        )
        return "\33[32m\33[1m\r " + str(formatted_msg) + " \n\33[0m"

    def format_msg_client_left(self, client_details,
                               message=messages['client-left']):
        log.debug('')
        formatted_msg = message[:]
        formatted_msg = formatted_msg.replace(
            '--client-details--', client_details
        )
        formatted_msg = formatted_msg.replace(
            '--client-count--', str(len(self.connected_list) - 2)
        )
        formatted_msg = formatted_msg.replace(
            '--capacity--', str(self.capacity)
        )
        return "\r\33[1m"+"\33[31m " + str(formatted_msg) + " \33[0m\n"

    def format_msg_client_offline(self, client_details, client_alias,
                                message=messages['client-offline']):
        log.debug('')
        formatted_msg = message[:]
        formatted_msg = formatted_msg.replace(
            '--timestamp--', str(
                datetime.datetime.now().strftime(self.timestamp_format)
            )
        )
        formatted_msg = formatted_msg.replace(
            '--client-details--', str(client_details)
        )
        formatted_msg = formatted_msg.replace(
            '--client-alias--', str(client_alias)
        )
        return str(formatted_msg)

    # HANDLERS

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def handle_abrupt_client_exit(self, sock):
        log.debug('TODO - FIX ME - Wont check out guest')
        try:
            (incomming_addr, port_number) = sock.getpeername()
        except Exception as e:
            log.warning(e)

            # TODO - Might work, might not
            del self.record[(incomming_addr, port_number)]
            self.connected_list.remove(sock)

            sock.close()
            return
        self.send_to_all(
            sock, self.format_msg_client_left_unexpectedly(
                self.record[(incomming_addr, port_number)]
            )
        )
        msg = self.format_msg_client_offline_error(
                (incomming_addr, port_number),
                self.record[(incomming_addr, port_number)]
            )
        if not self.silent:
            print(msg)
        log.info(msg)
        del self.record[(incomming_addr, port_number)]
        self.connected_list.remove(sock)
        sock.close()
        return 'continue'

    #@pysnooper.snoop()
    def handle_chatroom_new_connection(self, sock):
        log.debug('')
        sockfd, addr = self.server_socket.accept()
        name = sockfd.recv(self.room_buffer).decode()
        self.connected_list.append(sockfd)
        self.record[addr] = ""
        if name in self.record.values():
            sockfd.send(self.format_msg_username_taken().encode())
            del self.record[addr]
            self.connected_list.remove(sockfd)
            sockfd.close()
            return 'continue'
        else:
            self.record[addr]=name
            msg = self.format_msg_client_connected(addr, self.record[addr])
            if not self.silent:
                print(msg)
            log.info(msg)
            sockfd.send(self.format_msg_welcome(self.terminate_key).encode())
            self.send_to_all(sockfd, self.format_msg_client_joined(name))

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def handle_receive_data_from_client(self, sock):
        log.debug('')
        data1 = sock.recv(self.room_buffer).decode()
        data = data1[:data1.index("\n")]
        incomming_addr, port_number = sock.getpeername()
        if data == self.terminate_key:
            self.send_to_all(
                sock, self.format_msg_client_left(
                    self.record[(incomming_addr, port_number)]
                )
            )
            msg = self.format_msg_client_offline(
                    (incomming_addr, port_number),
                    self.record[(incomming_addr, port_number)]
                )
            if not self.silent:
                print(msg)
            log.info(msg)
            del self.record[(incomming_addr, port_number)]
            self.connected_list.remove(sock)
            sock.close()
            return 'continue'
        else:
            self.send_to_all(
                sock, self.format_msg_client_message(
                    self.record[(incomming_addr, port_number)], data
                )
            )

    #@pysnooper.snoop()
    def handle_chatroom_incomming_message(self, sock):
        log.debug('')
        try:
            return self.handle_receive_data_from_client(sock)
        except:
            return self.handle_abrupt_client_exit(sock)

    # SERVER

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def open_chatroom_server(self, stop_event):
        log.debug('')
        while not stop_event.wait(1):
            try:
                rList, wList, error_sockets = select.select(self.connected_list,[],[])
            except Exception as e:
                log.warning(e)
                break
            for sock in rList:
                if sock == self.server_socket:
                    handle = self.handle_chatroom_new_connection(sock)
                    if handle == 'continue':
                        continue
                else:
                    handle = self.handle_chatroom_incomming_message(sock)
                    if handle == 'continue':
                        continue

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def server_init(self, stop_event):
        log.debug('')
        self.refresh_im_server_values()
        try:
            self.server_socket.bind((self.address, self.port))
        except Exception as e:
            log.error(e)
            return False
        self.server_socket.listen(self.capacity)
        self.connected_list.append(self.server_socket)
        self.display_server_banner()
        try:
            self.open_chatroom_server(stop_event)
        finally:
            if hasattr(self.server_socket, '_sock'):
                self.server_socket._sock.close()
            self.server_socket.close()
            self.connected_list.remove(self.server_socket)

if __name__ == '__main__':
    im_chat_srv = PHChatServer()
    im_chat_srv.server_init()

