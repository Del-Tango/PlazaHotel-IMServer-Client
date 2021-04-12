#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# HOTEL

import logging
import pysnooper
import datetime
import threading
import socket

from .ph_chat_server import PHChatServer
from .ph_client import PHClient
from .ph_guest import PHGuest

log = logging.getLogger(__name__)


class PHRoom():

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        self.room_number = kwargs.get('room_number', str())
        self.floor_level = kwargs.get('floor_level', int())
        self.client = kwargs.get('client')
        self.guests = kwargs.get('guests', list())
        self.guest_list = kwargs.get('guest_list', list())
        self.capacity = kwargs.get('capacity', int())
        self.address = kwargs.get('address', '127.0.0.1')
        self.port_number = kwargs.get('port_number', 3000)
        self.timestamp = datetime.datetime.now()
        self.timestamp_format = kwargs.get(
            'timestamp_format', '%d/%m/%Y-%H:%M:%S'
        )
        self.silent = kwargs.get('silent', 'off')
        self.terminate_key = kwargs.get('terminate_key', '.terminate')
        self.floor_access_key = kwargs.get('floor_access_key', str())
        self.chat_server = self.spawn_chatroom_server()
        self.server_thread = None
        self.server_stop_event = threading.Event()
        self.online = False

    # FETCHERS

    def fetch_floor_access_key(self):
        log.debug('')
        return self.floor_access_key

    def fetch_client(self):
        log.debug('')
        return self.client

    def fetch_guest_creation_values(self, **kwargs):
        log.debug('')
        room_number, floor_level = self.fetch_room_number(), self.fetch_floor_level()
        allowed_rooms = kwargs.get('allowed_rooms', self.client.fetch_allowed_rooms())
        allowed_floors = kwargs.get('allowed_floors', self.client.fetch_allowed_floors())
        access_key = kwargs.get('access_key', self.client.fetch_access_key())
        return {
            'alias': kwargs.get('alias', 'Ghost'),
            'guest_of': self.client.fetch_alias(),
            'room_number': room_number,
            'floor_number': floor_level,
            'access_key': access_key,
            'allowed_rooms': allowed_rooms,
            'allowed_floors': allowed_floors,
        }

    def fetch_client_creation_values(self, **kwargs):
        log.debug('')
        room_number, floor = self.fetch_room_number(), self.fetch_floor_level()
        allowed_rooms = kwargs.get('allowed_rooms', [room_number])
        allowed_floors = kwargs.get('allowed_floors', [floor])
        access_key = kwargs.get('access_key', self.fetch_floor_access_key())
        return {
            'booked_floor': floor,
            'booked_room': room_number,
            'guest_limit': self.fetch_capacity() - 1,
            'allowed_rooms': allowed_rooms,
            'allowed_floors': allowed_floors,
            'superuser_flag': False,
            'access_key': access_key,
        }

    def fetch_terminate_key(self):
        log.debug('')
        return self.terminate_key

    def fetch_address(self):
        log.debug('')
        return self.address

    def fetch_server_stop_event(self):
        log.debug('')
        return self.server_stop_event

    def fetch_server_thread(self):
        log.debug('')
        return self.server_thread

    def fetch_online_flag(self):
        log.debug('')
        return self.online

    def fetch_timestamp_format(self):
        log.debug('')
        return self.timestamp_format

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def fetch_room_details(self):
        log.debug('')
        population = self.guests[:]
        if self.client:
            population.append(self.client)
        return {
            'room_number': self.room_number,
            'floor_level': self.floor_level,
            'client': self.client,
            'guests': self.guests,
            'guest_list': self.guest_list,
            'capacity': self.capacity,
            'port_number': self.port_number,
            'timestamp': self.timestamp.strftime(self.timestamp_format),
            'chat_server': self.chat_server,
            'timestamp_format': self.timestamp_format,
            'silent': self.silent,
            'terminate_key': self.terminate_key,
            'log_name': log.name,
            'online': self.online,
            'population': population,
        }

    def fetch_chat_server_creation_values(self, **kwargs):
        log.debug('')
        values = {
            'room_buffer': kwargs.get('room_buffer', 4096),
            'server_name': kwargs.get('server_name', 'PlazaHotel'),
            'address': kwargs.get('address', 'localhost'),
            'host': kwargs.get('host', self.fetch_address()),
            'port': kwargs.get('port', self.fetch_port_number()),
            'floor': kwargs.get('floor', self.fetch_floor_level()),
            'room': kwargs.get('room', self.fetch_room_number()),
            'capacity': kwargs.get('capacity', self.fetch_capacity()),
            'terminate_key': kwargs.get('terminate_key', '.exit'),
            'timestamp_format': kwargs.get(
                'timestamp_format', self.fetch_timestamp_format()
            ),
            'silent': kwargs.get('silent', self.fetch_silent_flag()),
            'log_name': log.name,
        }
        return values

    def fetch_floor_level(self):
        log.debug('')
        return self.floor_level

    def fetch_guests(self):
        log.debug('')
        return self.guests

    def fetch_guest_list(self):
        log.debug('')
        return self.guest_list

    def fetch_capacity(self):
        log.debug('')
        return self.capacity

    def fetch_port_number(self):
        log.debug('')
        return self.port_number

    def fetch_timestamp(self):
        log.debug('')
        return self.timestamp

    def fetch_chat_server(self):
        log.debug('')
        return self.chat_server

    def fetch_room_number(self):
        log.debug('')
        return self.room_number

    def fetch_terminate_key(self):
        log.debug('')
        return self.terminate_key

    def fetch_silent_flag(self):
        log.debug('')
        return self.silent

    # SETTERS

    def set_client(self, client_obj):
        log.debug('')
        if client_obj != None and not isinstance(client_obj, object):
            return self.error_invalid_client_object(client_obj)
        self.client = client_obj
        return self.client

    def set_terminate_key(self, terminate):
        log.debug('')
        if not isinstance(terminate, str):
            return self.error_invalid_terminate_key(terminate)
        self.terminate_key = terminate
        return self.terminate_key

    def set_address(self, address):
        log.debug('')
        if not isinstance(address, str):
            return self.error_invalid_server_address(address)
        self.address = address
        return self.address

    def set_server_stop_event(self, stop_event):
        log.debug('')
        self.server_stop_event = stop_event
        return self.server_stop_event

    def set_server_thread(self, server_thread):
        log.debug('')
        self.server_thread = server_thread
        return self.server_thread

    def set_online_flag(self, flag):
        log.debug('')
        if not isinstance(flag, bool):
            return self.error_invalid_online_flag(flag)
        self.online = flag
        return self.online

    def set_floor_level(self, level):
        log.debug('')
        if not isinstance(level, int):
            return self.error_invalid_floor_level(level)
        self.floor_level = level
        return self.floor_level

    def set_guests(self, guests):
        log.debug('')
        if not isinstance(guests, list):
            return self.error_invalid_guests(guests)
        self.guests = guests
        return self.guests

    def set_guest_list(self, guest_list):
        log.debug('')
        if not isinstance(guest_list, list):
            return self.error_invalid_guest_list(guest_list)
        self.guest_list = guest_list
        return self.guest_list

    def set_capacity(self, capacity):
        log.debug('')
        if not isinstance(capacity, int):
            return self.error_invalid_room_capacity(capacity)
        self.capacity = capacity
        return self.capacity

    def set_port_number(self, port_number):
        log.debug('')
        if not isinstance(port_number, int):
            return self.error_invalid_port_number(port_number)
        self.port_number = port_number
        return self.port_number

    def set_timestamp(self, timestamp):
        log.debug('')
        self.timestamp = timestamp
        return self.timestamp

    def set_chat_server(self, chat_server):
        log.debug('')
        if not isinstance(chat_server, object):
            return self.error_invalid_chat_server(chat_server)
        self.chat_server = chat_server
        return self.chat_server

    def set_room_number(self, room_number):
        log.debug('')
        if not isinstance(room_number, int):
            return self.error_invalid_room_number(room_number)
        self.room_number = room_number
        return self.room_number

    def set_terminate_key(self, terminate_key):
        log.debug('')
        if not isinstance(terminate_key, str):
            return self.error_invalid_terminate_key(terminate_key)
        self.terminate_key = terminate_key
        return self.terminate_key

    def set_silent_flag(self, flag):
        log.debug('')
        if not isinstance(flag, bool):
            return self.error_invalid_silent_flag(flag)
        self.silent = flag
        return self.silent

    def set_timestamp_format(self, timestamp_format):
        log.debug('')
        if not isinstance(timestamp_format, str):
            return self.error_invalid_timestamp_format(timestamp_format)
        self.timestamp_format = timestamp_format
        return self.timestamp_format

    # UPDATERS

    def update_guests(self, guest_obj):
        log.debug('')
        active_guests = self.fetch_guests()[:]
        active_guests.append(guest_obj)
        return self.set_guests(active_guests)

    # CHECKERS

    def check_online(self):
        log.debug('')
        return self.fetch_online_flag()

#   @pysnooper.snoop('logs/plaza-hotel.log')
    def check_alias_in_guest_list(self, alias):
        log.debug('')
        guest_list = self.fetch_guest_list()
        if not guest_list:
            return True
        return alias in guest_list

    # SPAWNERS

#   @pysnooper.snoop()
    def spawn_chatroom_server(self):
        log.debug('')
        creation_values = self.fetch_chat_server_creation_values()
        return self.create_chatroom_server(creation_values)

#   @pysnooper.snoop()
    def spawn_guest(self, guest_alias, **kwargs):
        log.debug('')
        creation_values = self.fetch_guest_creation_values(
            alias=guest_alias, **kwargs
        )
        return self.create_guest(creation_values)

    def spawn_client(self, client_alias):
        log.debug('')
        creation_values = self.fetch_client_creation_values()
        creation_values.update({'alias': client_alias})
        return self.create_client(creation_values)

    # CREATORS

    def create_server_stop_event(self):
        log.debug('')
        return threading.Event()

    def create_guest(self, creation_values):
        log.debug('')
        try:
            return PHGuest(**creation_values)
        except Exception as e:
            return self.error_could_not_create_guest(creation_values, e)

    def create_client(self, creation_values):
        log.debug('')
        try:
            return PHClient(**creation_values)
        except Exception as e:
            return self.error_could_not_create_client(creation_values, e)

    def create_chatroom_server(self, creation_values):
        log.debug('')
        try:
            return PHChatServer(**creation_values)
        except Exception as e:
            return self.error_could_not_create_instant_messaging_server(
                creation_values, e
            )

    # FORMATTERS

    def format_room_detail_string(self):
        log.debug('')
        details = '<(Room)- Level: {}, Room Number: {}, Online: {}, '\
            'Client: {}, Guest Count: {}>'.format(
                self.floor_level, self.room_number, self.online,
                self.client, len(self.guests)
            )
        return details

    # OVERRIDES

    def __str__(self, *args, **kwargs):
        log.debug('')
        return self.format_room_detail_string()

    # GENERAL

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def guest_join(self, guest_alias, **kwargs):
        log.debug('')
        check = self.check_alias_in_guest_list(guest_alias)
        if not check:
            return self.warning_alias_not_in_guest_list(guest_alias, check)
        if not self.fetch_guest_list() and self.fetch_floor_level() != 0:
            if not kwargs.get('instruction_set'):
                return self.warning_open_room_join_requires_access_key(
                    guest,alias, check, kwargs
                )
            if kwargs['instruction_set'][3] != self.client.fetch_access_key():
                return self.warning_invalid_floor_access_key(
                    guest_alias, kwargs, check
                )
        guest_obj = self.spawn_guest(guest_alias, **kwargs)
        if not guest_obj:
            return self.warning_invalid_room_orbital_details(
                guest_alias, kwargs, guest_obj
            )
        self.update_guests(guest_obj)
        return guest_obj

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def terminate_chatroom_server(self):
        log.debug('')
        try:
            port_number, address = self.fetch_port_number(), self.fetch_address()
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((address, port_number))
            server_socket.send(self.fetch_terminate_key().encode())
        except Exception as e:
            log.error(e)
        finally:
            server_socket.close()
        return True

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def stop_chatroom_server(self):
        log.debug('')
        server_thread = self.fetch_server_thread()
        stop_event = self.fetch_server_stop_event()
        if not server_thread:
            return self.error_no_chat_server_thread_found(server_thread)
        stop_event.set()
        self.terminate_chatroom_server()
        server_thread.join()
        self.set_online_flag(False)
        self.set_server_thread(None)
        return True

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def client_checkout(self, client_alias, **kwargs):
        log.debug('')
        if not self.client:
            return False
        if client_alias == self.client.fetch_alias():
            set_client = self.set_client(None)
            set_guest_list = self.set_guest_list([])
            set_guests = self.set_guests([])
            return self.stop_chatroom_server()
        for guest in self.guests:
            if client_alias == guest.fetch_alias():
                self.guests.remove(guest)
                break
        else:
            return self.warning_client_not_in_orbit(client_alias)
        return True


#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def client_checkin(self, client_alias, **kwargs):
        log.debug('')
        client_obj = self.spawn_client(client_alias)
        guest_list = kwargs.get('guest_list', list())
        set_client = self.set_client(client_obj)
        set_guest_list = self.set_guest_list(guest_list)
        if not set_client or not isinstance(set_guest_list, list):
            return self.warning_invalid_room_orbital_details(
                client_alias, kwargs, client_obj, guest_list,
                set_client, set_guest_list
            )
        self.start_chatroom_server()
        return client_obj

    def start_chatroom_server(self):
        log.debug('')
        im_server = self.fetch_chat_server()
        self.set_online_flag(True)
        return self.init_server_thread(im_server)

    # INIT

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def init_server_thread(self, im_server):
        log.debug('')
        im_server = im_server or self.fetch_chat_server()
        stop_event = self.set_server_stop_event(
            self.create_server_stop_event()
        )
        thread = threading.Thread(
            target=im_server.server_init, args=(stop_event,)
        )
        thread.daemon = True
        thread.start()
        return self.set_server_thread(thread)

    # WARNINGS

    def warning_open_room_join_requires_access_key(self, *args):
        log.warning('Open room join requires access key. Details: {}'.format(args))
        return False

    def warning_alias_not_in_guest_list(self, *args):
        log.warning('Alias not on guest list. Details: {}'.format(args))
        return False

    def warning_client_not_in_orbit(self, *args):
        log.warning('Client not in orbit. Details: {}'.format(args))
        return False

    def warning_invalid_room_orbital_details(self, *args):
        log.warning('Invalid room orbital details. Details: {}'.format(args))
        return False

    # ERRORS

    def error_invalid_client_object(self, *args):
        log.error('Invalid client object. Details: {}'.format(args))
        return False

    def error_invalid_server_address(self, *args):
        log.error('Invalid server address. Details: {}'.format(args))
        return False

    def error_no_chat_server_thread_found(self, *args):
        log.error('No IM chat server thread found. Details: {}'.format(args))
        return False

    def error_invalid_online_flag(self, *args):
        log.error('Invalid online flag. Details: {}'.format(args))
        return False

    def error_could_not_create_client(self, *args):
        log.error(
            'Something went wrong. '
            'Could not create client in room {}, level {}. '
            'Details: {}'.format(
                self.fetch_room_number(), self.fetch_floor_level(), args
            )
        )
        return False

    def error_could_not_create_guest(self, *args):
        log.error(
            'Something went wrong. '
            'Could not create guest in room {}, level {}. '
            'Details: {}'.format(
                self.fetch_room_number(), self.fetch_floor_level(), args
            )
        )
        return False

    def error_invalid_guest_list(self, *args):
        log.error('Invalid guest list. Details: {}'.format(args))
        return False

    def error_invalid_room_capacity(self, *args):
        log.error('Invalid room capacity. Details: {}'.format(args))
        return False

    def error_invalid_port_number(self, *args):
        log.error('Invalid port number. Details: {}'.format(args))
        return False

    def error_invalid_timestamp_format(self, *args):
        log.error('Invalid timestamp format. Details: {}'.format(args))
        return False

    def error_invalid_silent_flag(self, *args):
        log.error('Invalid silent flag. Details: {}'.format(args))
        return False

    def error_invalid_terminate_key(self, *args):
        log.error('Invalid chat termination key. Details: {}'.format(args))
        return False

    def error_invalid_room_number(self, *args):
        log.error('Invalid room number. Details: {}'.format(args))
        return False

    def error_invalid_chat_server(self, *args):
        log.error('Invalid instant messaging server. Details: {}'.format(args))
        return False

    def error_invalid_guests(self, *args):
        log.error('Invalid guest set. Details: {}'.format(args))
        return False

    def error_invalid_floor_level(self, *args):
        log.error('Invalid floor level. Details: {}'.format(args))
        return False

    def error_could_not_create_instant_messaging_server(self, *args):
        log.error(
            'Something went wrong. '
            'Could not instantiate instant messaging server for room {} on level {}. '
            'Details: {}'.format(
                self.fetch_room_number(), self.fetch_floor_level(), args
            )
        )
        return False
