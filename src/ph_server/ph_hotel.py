#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# HOTEL

import os
import datetime
import stat
import random
import string
import logging
import pysnooper

from .ph_floor import PHFloor
from .ph_writter import PHFileWritter

log = logging.getLogger(__name__)


class PHHotel(object):

    state_file_separators = {
        'floors': ('[[ FLOORS  ]]\n', '\n[[ ' + '_' * 7 + ' ]]'),
        'rooms': ('[[ ROOMS   ]]\n', '\n[[ ' + '_' * 7 + ' ]]'),
        'clients': ('[[ CLIENTS ]]\n', '\n[[ ' + '_' * 7 + ' ]]'),
        'guests': ('[[ GUESTS  ]]\n', '\n[[ ' + '_' * 7 + ' ]]'),
    }

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        self.hotel_name = kwargs.get('hotel_name', 'PlazaHotel')
        self.hotel_floors = kwargs.get('hotel_floors', dict())
        self.hotel_map = kwargs.get('hotel_map', list())
        self.floor_access_keys = kwargs.get('floor_access_keys', dict())
        self.hotel_orbitals = kwargs.get('hotel_orbitals', list())
        self.state_file = kwargs.get('state_file', str())
        self.state_fifo = kwargs.get('state_fifo', str())
        self.response_fifo = kwargs.get('response_fifo', str())
        self.state_map = kwargs.get('state_map', dict())
        self.floor_count = kwargs.get('floor_count', int())
        self.room_count = kwargs.get('room_count', int())
        self.room_capacity = kwargs.get('room_capacity', int())
        self.key_file = kwargs.get('key_file', str())
        self.timestamp = datetime.datetime.now()
        self.state_writter = PHFileWritter(**{
            'file_path': self.state_file,
            'log_name': log.name,
        })
        self.silent = kwargs.get('silent', 'off')
        self.timestamp_format = kwargs.get('timestamp_format', '%d/%m/%Y-%H:%M:%S')
        self.address = kwargs.get('address', '127.0.0.1')
        self.port_number = kwargs.get('port_number', 3000)
        self.file_permissions = kwargs.get('file_permissions', 750)

    # FETCHERS

    def fetch_floor_rooms_from_state_file_content(self, floor_level,
                                                    state_file_lines):
        log.debug('')
        room_lines = self.filter_room_lines_from_state_file_content(
            state_file_lines
        )
        rooms = []
        for line in room_lines:
            try:
                segmented_line = line.split(' ')
                room_number = segmented_line[0]
                timestamp = segmented_line[1]
                floor_number = segmented_line[2]
                port_number = segmented_line[3]
                capacity = segmented_line[4]
                cortex = segmented_line[5]
                orbitals = [] if len(segmented_line) >= 6 else segmented_line[6:]
            except Exception as e:
                self.warning_malformed_state_file_guest_line(line, e)
                continue
            if floor_number != floor_level:
                continue
            rooms.append(room_number)
        return self.format_room_map(rooms)

    def fetch_client_guests_from_state_file_content(self, client_alias,
                                                    state_file_lines):
        log.debug('')
        guest_lines = self.filter_guest_lines_from_state_file_content(
            state_file_lines
        )
        guests = []
        for line in guest_lines:
            try:
                segmented_line = line.split(' ')
                guest_alias = segmented_line[0]
                timestamp = segmented_line[1]
                host_alias = segmented_line[2]
                room_number = segmented_line[3]
                floor_number = segmented_line[4]
            except Exception as e:
                self.warning_malformed_state_file_guest_line(line, e)
                continue
            if host_alias != client_alias:
                continue
            guests.append(guest_alias)
        return guests

    def fetch_floor_access_key(self, floor_number):
        log.debug('')
        floor = self.search_floor_by_number(floor_number)
        if not floor:
            return floor
        return floor.fetch_access_key()

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def fetch_server_state_floors(self):
        log.debug('')
        floor_states, hotel_floors = {}, self.fetch_hotel_floors()
        for floor in hotel_floors:
            details = hotel_floors[floor].fetch_floor_details()
            floor_states.update({
                details.get('level', ' '): {
                    'timestamp': details.get('timestamp', ' '),
                    'room_count': details.get('room_count', ' '),
                    'user_count': details.get('user_count', ' '),
                    'rooms': details.get('rooms', {}),
                    'protected': 'protected' if details.get('access_key')
                        else 'unprotected',
                }
            })
        return floor_states

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def fetch_server_state_clients(self):
        log.debug('')
        client_states, hotel_orbitals = {}, self.fetch_hotel_orbitals()
        if not hotel_orbitals:
            return {}
        for orbital in hotel_orbitals:
            if not orbital.is_client():
                continue
            details = orbital.fetch_values()
            room = self.search_room_by_number(details.get('booked_room'))
            if not room:
                continue
            room_details = room.fetch_room_details()
            client_states.update({
                details.get('alias', ' '): {
                    'timestamp': details.get('timestamp', ' '),
                    'booked_room': details.get('booked_room', ' '),
                    'booked_floor': details.get('booked_floor', ' '),
                    'guest_list': room_details.get('guest_list', []),
                    'guest_count': len(room_details.get('guests', [])),
                    'guests': [
                        guest.fetch_alias()
                        for guest in room_details.get('guests', [])
                    ]
                }
            })
        return client_states

    def fetch_key_file(self):
        log.debug('')
        return self.key_file

    def fetch_response_fifo(self):
        log.debug('')
        return self.response_fifo

    def fetch_floor_creation_values(self, floor_level, **kwargs):
        log.debug('')
        if not isinstance(floor_level, int):
            return self.error_invalid_floor_level(floor_level, kwargs)
        return {
            'level': floor_level,
            'rooms': kwargs.get('rooms', {}),
            'orbitals': kwargs.get('orbitals', []),
            'log_name': log.name,
        }

    def fetch_server_state_details(self):
        log.debug('')
        return {
            'floors': self.fetch_server_state_floors(),
            'rooms': self.fetch_server_state_rooms(),
            'clients': self.fetch_server_state_clients(),
            'guests': self.fetch_server_state_guests(),
        }

#   @pysnooper.snoop()
    def fetch_server_state_rooms(self):
        log.debug('')
        room_states, hotel_floors = {}, self.fetch_hotel_floors()
        for floor in hotel_floors:
            floor_details = hotel_floors[floor].fetch_floor_details()
            floor_rooms = floor_details.get('rooms', {})
            for room in floor_rooms:
                details = floor_rooms[room].fetch_room_details()
                is_open = 'open-cortex' if not details.get('guest_list') \
                    else 'closed-cortex'
                room_states.update({
                    details['room_number']: {
                        'timestamp': details.get('timestamp', ' '),
                        'port_number': details.get('port_number', ' '),
                        'capacity': details.get('capacity', ' '),
                        'floor_level': details.get('floor_level', ' '),
                        'population': [
                            user.fetch_alias() for user in
                            details.get('population', [])[::-1]
                        ],
                        'cortex': is_open,
                    }
                })
        return room_states

    def fetch_server_state_guests(self):
        log.debug('')
        client_states, hotel_orbitals = {}, self.fetch_hotel_orbitals()
        for orbital in hotel_orbitals:
            if not orbital.is_guest():
                continue
            details = orbital.fetch_details()
            client_states.update({
                details.get('alias', ' '): {
                    'timestamp': details.get('timestamp', ' '),
                    'guest_of': details.get('guest_of', ' '),
                    'room_number': details.get('room_number', ' '),
                    'floor_number': details.get('floor_number', ' '),
                }
            })
        return client_states

    def fetch_server_address(self):
        log.debug('')
        return self.address

    def fetch_server_port_number(self):
        log.debug('')
        return self.port_number

    def fetch_room_creation_values(self, **kwargs):
        log.debug('')
        return {
            'address': kwargs.get('address', self.fetch_server_address()),
            'room_number': kwargs.get('room_number', int()),
            'floor_level': kwargs.get('floor_level', int()),
            'access_key': self.fetch_floor_access_key(kwargs.get('floor_level', int())),
            'port_number': kwargs.get('port_number', self.fetch_server_port_number()),
            'capacity': kwargs.get('capacity', self.fetch_room_capacity()),
            'timestamp_format': kwargs.get(
                'timestamp_format', self.fetch_timestamp_format()
            ),
            'silent': kwargs.get('silent', self.fetch_silent_flag()),
            'log_name': log.name,
        }

    def fetch_timestamp_format(self):
        log.debug('')
        return self.timestamp_format

    def fetch_silent_flag(self):
        log.debug('')
        return self.silent

    def fetch_floor_access_keys(self):
        log.debug('')
        return self.floor_access_keys

    def fetch_timestamp(self):
        log.debug('')
        return self.timestamp

    def fetch_hotel_map(self):
        log.debug('')
        if not self.hotel_map:
            self.set_hotel_map(self.build_hotel_map())
        return self.hotel_map

    def fetch_floor_count(self):
        log.debug('')
        return self.floor_count

    def fetch_room_count(self):
        log.debug('')
        return self.room_count

    def fetch_room_capacity(self):
        log.debug('')
        return self.room_capacity

    def fetch_hotel_orbitals(self):
        log.debug('')
        return self.hotel_orbitals

    def fetch_hotel_floors(self):
        log.debug('')
        return self.hotel_floors

    def fetch_state_file_separators(self):
        log.debug('')
        return self.state_file_separators

    def fetch_state_separator(self, state, position):
        log.debug('')
        separators = self.fetch_state_file_separators()
        if state not in separators:
            return self.error_invalid_state_file_separator_label(
                state, position, separators
            )
        elif position not in ('start', 'end'):
            return self.error_invalid_state_separator_position(
                state, position, separators
            )
        pos_index = 0 if position == 'start' else 1
        return separators[state][pos_index]

    def fetch_state_writter(self):
        log.debug('')
        if not self.state_writter:
            file_writter = self.create_state_file_writter(
                file_path=self.fetch_state_file()
            )
            self.set_state_writter(file_writter)
        return self.state_writter

    def fetch_state_file(self):
        log.debug('')
        return self.state_file

    def fetch_state_fifo(self):
        log.debug('')
        return self.state_fifo

    def fetch_state_map(self):
        log.debug('')
        return self.state_map

    # SETTERS

    def set_key_file(self, file_path):
        log.debug('')
        self.key_file = file_path
        self.update_timestamp()
        return self.key_file

    def set_response_fifo(self, response_fifo):
        log.debug('')
        self.response_fifo = response_fifo
        self.update_timestamp()
        return self.response_fifo

    def set_state_fifo(self, state_fifo):
        log.debug('')
        self.state_fifo = state_fifo
        self.update_timestamp()
        return self.state_fifo

    def set_state_file(self, state_file):
        log.debug('')
        self.state_file = state_file
        self.update_timestamp()
        return self.state_file

    def set_floor_access_keys(self, floor_access_keys):
        log.debug('')
        if not isinstance(floor_access_keys, dict):
            return self.error_invalid_floor_access_keys(floor_access_keys)
        self.floor_access_keys = floor_access_keys
        self.update_timestamp()
        return self.floor_access_keys

    def set_room_count(self, count):
        log.debug('')
        if not isinstance(count, int):
            return self.error_invalid_hotel_room_count(count)
        self.room_count = count
        self.update_timestamp()
        return self.room_count

    def set_floor_count(self, count):
        log.debug('')
        if not isinstance(count, int):
            return self.error_invalid_hotel_floor_count(count)
        self.floor_count = count
        self.update_timestamp()
        return self.floor_count

    def set_timestamp(self, timestamp):
        log.debug('')
        self.timestamp = timestamp
        return self.timestamp

    def set_hotel_map(self, hotel_map):
        log.debug('')
        if not isinstance(hotel_map, list):
            return self.error_invalid_hotel_map(hotel_map)
        self.hotel_map = hotel_map
        self.update_timestamp()
        return self.hotel_map

    def set_state_writter(self, state_writter):
        log.debug('')
        self.state_writter = state_writter
        self.update_timestamp()
        return self.state_writter

    def set_state_map(self, state_map):
        log.debug('')
        self.state_map = state_map
        self.update_timestamp()
        return self.state_map

    # CHECKERS

    def check_alias_registered(self, alias):
        log.debug('')
        orbital_aliases = [
            orbital.fetch_alias() for orbital in
            self.fetch_hotel_orbitals()
        ]
        return True if alias in orbital_aliases else False

    def check_file_exists(self, file_path):
        log.debug('')
        return os.path.isfile(file_path)

    def check_fifo_exists(self, pipe_path):
        log.debug('')
        return stat.S_ISFIFO(os.stat(pipe_path).st_mode)

    def check_state_file_exist(self):
        log.debug('')
        return self.check_file_exists(self.fetch_state_file())

    def check_state_fifo_exists(self):
        log.debug('')
        return self.check_fifo_exists(self.fetch_state_fifo())

    # UPDATERS

    def update_orbitals(self, orbital_user):
        log.debug('')
        if not isinstance(orbital_user, object):
            return self.error_invalid_orbital(orbital_user)
        self.hotel_orbitals.append(orbital_user)
        self.update_timestamp()
        return self.hotel_orbitals

    def update_timestamp(self):
        log.debug('')
        return self.set_timestamp(datetime.datetime.now())

    def update_floors(self, floor_map):
        log.debug('')
        if not isinstance(floor_map, dict):
            return self.error_invalid_floor_map(floor_map)
        self.hotel_floors.update(floor_map)
        self.update_timestamp()
        return self.hotel_floors

    def update_hotel_map(self, hotel_map=None):
        log.debug('')
        if not hotel_map:
            hotel_map = self.build_hotel_map()
        return self.set_hotel_map(hotel_map)

    def update_state_map(self, state_map):
        log.debug('')
        return self.state_map.update(state_map)

    # BUILDERS

    def build_hotel_map(self):
        log.debug('')
        floor_count = self.fetch_floor_count()
        room_count = self.fetch_room_count()
        hotel_floors = self.fetch_hotel_floors()
        hotel_map = [
            [(None,) for x in range(room_count)]
            for y in range(floor_count + 1)
        ]
        for floor in hotel_floors:
            room_count = 0
            for room in hotel_floors[floor].rooms:
                room_number = hotel_floors[floor].rooms[room].room_number
                online = hotel_floors[floor].rooms[room].online
                formatted_online = 'occupied' if online else 'vacant'
                client = formatted_online if not online \
                    or not hotel_floors[floor].rooms[room].client \
                    else hotel_floors[floor].rooms[room].client.fetch_alias()
                guests = [
                    guest.fetch_alias() for guest in
                    hotel_floors[floor].rooms[room].guests
                ]
                port = hotel_floors[floor].rooms[room].port_number
                hotel_map[floor][room_count] = (
                    room_number, client, port, guests
                )
                room_count += 1
        return hotel_map

    def build_state_map(self):
        log.debug('')
        return self.fetch_server_state_details()

    # FILTERS

    def filter_state_file_lines_trimmed(self, start_pattern, end_pattern, state_file_content):
        log.debug('')
        filtered_lines, start_line, end_line = [], 0, 0
        start_reached, end_reached = False, False,
        for line_index in range(len(state_file_content) - 1):
            if not start_reached:
                if not state_file_content[line_index] == start_reached:
                    continue
                start_reached, start_line = True, line_index
                continue
            if end_reached:
                break
            elif state_file_content[line_index] == end_reached:
                end_reached, end_line = True, line_index - 1
                continue
            elif not state_file_content[line_index] or state_file_content[line_index][0] == '#':
                continue
            filtered_lines.append(state_file_content[line_index])
        return {
            'filtered': filtered_lines,
            'start_line': start_line + 1,
            'end_line': end_line + 1,
        }

    def filter_floor_lines_from_state_file_content(self, state_file_content):
        log.debug('')
        start_marker = self.fetch_state_separator('floors', 'start'), 0
        end_marker = self.fetch_state_separator('floors', 'end'), 0
        floor_lines = self.filter_state_file_lines_trimmed(
            start_marker, end_marker, state_file_content
        )
        return floor_lines['filtered']

    def filter_room_lines_from_state_file_content(self, state_file_content):
        log.debug('')
        start_marker = self.fetch_state_separator('rooms', 'start'), 0
        end_marker = self.fetch_state_separator('rooms', 'end'), 0
        room_lines = self.filter_state_file_lines_trimmed(
            start_marker, end_marker, state_file_content
        )
        return room_lines['filtered']

    def filter_client_lines_from_state_file_content(self, state_file_content):
        log.debug('')
        start_marker = self.fetch_state_separator('clients', 'start'), 0
        end_marker = self.fetch_state_separator('clients', 'end'), 0
        client_lines = self.filter_state_file_lines_trimmed(
            start_marker, end_marker, state_file_content
        )
        return client_lines['filtered']

    def filter_guest_lines_from_state_file_content(self, state_file_content):
        log.debug('')
        start_marker = self.fetch_state_separator('guests', 'start')
        end_marker = self.fetch_state_separator('guests', 'end')
        guest_lines = self.filter_state_file_lines_trimmed(
            start_marker, end_marker, state_file_content
        )
        return guest_lines['filtered']

    # FORMATTERS

    def format_key_file_content_from_key_map(self, key_map):
        log.debug('')
        if not isinstance(key_map, dict):
            return self.error_invalid_level_access_key_map(key_map)
        content = []
        for floor_number, access_key in key_map.items():
            content.append('{} {}'.format(floor_number, access_key))
        if not content:
            self.warning_no_key_file_content_formatted(key_map, content)
        return content

    def format_room_map(self, room_numbers):
        log.debug('')
        room_map = {}
        for room_number in room_numbers:
            room = self.search_room_by_number(room_number)
            if not room:
                continue
            room_map.update({room_number: room})
        return room_map

    def format_state_map_floors_from_state_file_content(self, state_file_lines):
        log.debug('')
        floor_lines = self.filter_floor_lines_from_state_file_content(state_file_lines)
        floor_states = {}
        for line in floor_lines:
            try:
                segmented_line = line.split(' ')
                floor_level = segmented_line[0]
                timestamp = segmented_line[1]
                room_count = segmented_line[2]
                orbital_count = segmented_line[3]
                access_flag = segmented_line[4]
                rooms = self.fetch_floor_rooms_from_state_file_content(
                    floor_level, state_file_lines
                )
            except Exception as e:
                self.warning_malformed_state_file_floor_line(line, e)
            floor_states.update({
                floor_level: {
                    'timestamp': timestamp,
                    'room_count': room_count,
                    'user_count': orbital_count,
                    'rooms': rooms,
                    'protected': access_flag,
                }
            })
        return floor_states

    def format_state_map_rooms_from_state_file_content(self, state_file_lines):
        log.debug('')
        room_lines = self.filter_room_lines_from_state_file_content(state_file_lines)
        room_states = {}
        for line in room_lines:
            try:
                segmented_line = line.split(' ')
                room_number = segmented_line[0]
                timestamp = segmented_line[1]
                floor_number = segmented_line[2]
                port_number = segmented_line[3]
                capacity = segmented_line[4]
                cortex = segmented_line[5]
                orbitals = [] if len(segmented_line) <= 6 else segmented_line[6:]
            except Exception as e:
                self.warning_malformed_state_file_room_line(line, e)
            room_states.update({
                room_number: {
                    'timestamp': timestamp,
                    'port_number': port_number,
                    'capacity': capacity,
                    'floor_level': floor_number,
                    'population': orbitals,
                    'cortex': cortex,
                }
            })
        return room_states

    def format_state_map_clients_from_state_file_content(self, state_file_lines):
        log.debug('')
        client_lines = self.filter_client_lines_from_state_file_content(state_file_lines)
        client_states = {}
        for line in client_lines:
            try:
                segmented_line = line.split(' ')
                client_alias = segmented_line[0]
                timestamp = segmented_line[1]
                room_number = segmented_line[2]
                floor_number = segmented_line[3]
                active_guests = segmented_line[4]
                guest_list = [] if len(segmented_line) <= 5 else segmented_line[5:]
                guests = self.fetch_client_guests_from_state_file_content(
                    client_alias, state_file_lines
                )
            except Exception as e:
                self.warning_malformed_state_file_client_line(line, e)
            client_states.update({
                client_alias: {
                    'timestamp': timestamp,
                    'booked_room': room_number,
                    'booked_floor': floor_number,
                    'guest_list': guest_list,
                    'guest_count': active_guests,
                    'guests': guests,
                }
            })
        return client_states

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def format_state_map_guests_from_state_file_content(self, state_file_lines):
        log.debug('')
        guest_lines = self.filter_guest_lines_from_state_file_content(state_file_lines)
        guest_states = {}
        for line in guest_lines:
            try:
                segmented_line = line.split(' ')
                guest_alias = segmented_line[0]
                timestamp = segmented_line[1]
                guest_of = segmented_line[2]
                room_number = segmented_line[3]
                floor_number = segmented_line[4]
            except Exception as e:
                self.warning_malformed_state_file_guest_line(line, e)
                continue
            guest_states.update({
                guest_alias: {
                    'timestamp': timestamp,
                    'guest_of': guest_of,
                    'room_number': room_number,
                    'floor_number': floor_number,
                }
            })
        return guest_states

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def format_state_map_from_state_file_content(self, state_file_lines):
        log.debug('')
        state_map = {
            'floors': self.format_state_map_floors_from_state_file_content(state_file_lines),
            'rooms': self.format_state_map_rooms_from_state_file_content(state_file_lines),
            'clients': self.format_state_map_clients_from_state_file_content(state_file_lines),
            'guests': self.format_state_map_guests_from_state_file_content(state_file_lines),
        }
        return state_map

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def format_state_file_content_guests_from_state_map(self, state_map):
        log.debug('')
        mapped_guests, file_lines = state_map.get('guests', {}), []
        start_marker = self.fetch_state_separator('guests', 'start')
        end_marker = self.fetch_state_separator('guests', 'end')
        file_lines.append(start_marker)
        for guest in mapped_guests:
            file_line = '{} {} {} {} {} $'.format(
                guest, mapped_guests[guest]['timestamp'],
                mapped_guests[guest]['guest_of'],
                mapped_guests[guest]['room_number'],
                mapped_guests[guest]['floor_number'],
            )
            file_lines.append(file_line)
        file_lines.append(end_marker)
        return file_lines

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def format_state_file_content_clients_from_state_map(self, state_map):
        log.debug('')
        mapped_clients, file_lines = state_map.get('clients', {}), []
        start_marker = self.fetch_state_separator('clients', 'start')
        end_marker = self.fetch_state_separator('clients', 'end')
        file_lines.append(start_marker)
        for client in mapped_clients:
            guest_string = ' '.join(mapped_clients[client]['guest_list'])
            file_line = '{} {} {} {} {} {} $'.format(
                client, mapped_clients[client]['timestamp'],
                mapped_clients[client]['booked_room'],
                mapped_clients[client]['booked_floor'],
                mapped_clients[client]['guest_count'],
                guest_string,
            )
            file_lines.append(file_line)
        file_lines.append(end_marker)
        return file_lines

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def format_state_file_content_floors_from_state_map(self, state_map):
        log.debug('')
        mapped_floors, file_lines = state_map.get('floors', {}), []
        start_marker = self.fetch_state_separator('floors', 'start')
        end_marker = self.fetch_state_separator('floors', 'end')
        file_lines.append(start_marker)
        for floor in mapped_floors:
            file_line = '{} {} {} {} {} $'.format(
                floor, mapped_floors[floor]['timestamp'],
                mapped_floors[floor]['room_count'],
                mapped_floors[floor]['user_count'],
                mapped_floors[floor]['protected'],
            )
            file_lines.append(file_line)
        file_lines.append(end_marker)
        return file_lines

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def format_state_file_content_rooms_from_state_map(self, state_map):
        log.debug('')
        mapped_rooms, file_lines = state_map.get('rooms', {}), []
        start_marker = self.fetch_state_separator('rooms', 'start')
        end_marker = self.fetch_state_separator('rooms', 'end')
        file_lines.append(start_marker)
        for room in mapped_rooms:
            file_line = '{} {} {} {} {} {} {} $'.format(
                room, mapped_rooms[room]['timestamp'],
                mapped_rooms[room]['floor_level'],
                mapped_rooms[room]['port_number'],
                mapped_rooms[room]['capacity'],
                mapped_rooms[room]['cortex'],
                ' '.join(mapped_rooms[room]['population']),
            )
            file_lines.append(file_line)
        file_lines.append(end_marker)
        return file_lines

    def format_state_file_content_from_state_map(self, state_map):
        log.debug('')
        sections = {
            'floors': self.format_state_file_content_floors_from_state_map(state_map),
            'rooms': self.format_state_file_content_rooms_from_state_map(state_map),
            'clients': self.format_state_file_content_clients_from_state_map(state_map),
            'guests': self.format_state_file_content_guests_from_state_map(state_map),
        }

        log.debug('\n\nSTATE MAP: {}\n'.format(state_map))

        content = []
        for section in sections:
            content += sections[section]
        return content

    def format_hotel_detail_string(self):
        log.debug('')
        details = '<({})- State File: {}, State FIFO: {}, State Writter: {}>'\
            .format(
                self.hotel_name, self.state_file, self.state_fifo,
                self.state_writter
            )
        return details

    # ENSURANCE

    # TODO
    def ensure_state_from_map(self, state_map):
        log.debug('TODO - Under construction, building...')
        return False

    def ensure_text_file_exists(self, file_path):
        log.debug('')
        try:
            if not os.path.exists(file_path):
                f = open(file_path, 'w')
                f.close()
                os.chmod(file_path, self.file_permissions)

        except Exception as e:
            return self.error_could_not_ensure_text_file_exists(file_path, e)
        return True

    def ensure_fifo_exists(self, fifo_path):
        log.debug('')
        try:
            os.mkfifo(fifo_path)
            os.chmod(fifo_path, self.file_permissions)
        except Exception as e:
            return self.error_could_not_ensure_fifo_exists(fifo_path, e)
        return True

    def ensure_key_file_exists(self):
        log.debug('')
        return self.ensure_text_file_exists(self.fetch_key_file())

    def ensure_state_file_exists(self):
        log.debug('')
        return self.ensure_text_file_exists(self.fetch_state_file())

    def ensure_state_fifo_exists(self):
        log.debug('')
        return self.ensure_fifo_exists(self.fetch_state_fifo())

    def ensure_response_fifo_exists(self):
        log.debug('')
        return self.ensure_fifo_exists(self.fetch_response_fifo())

    def ensure_files_exist(self):
        log.debug('')
        return {
            'state_file': self.ensure_state_file_exists(),
            'key_file': self.ensure_key_file_exists(),
            'state_fifo': self.ensure_state_fifo_exists(),
            'response_fifo': self.ensure_response_fifo_exists(),
        }

    # CREATORS

    def create_hotel_floor(self, floor_level, **kwargs):
        log.debug('')
        creation_values = self.fetch_floor_creation_values(floor_level, **kwargs)
        return PHFloor(**creation_values)

    def create_state_file_writter(self, file_path=None, file_content=None):
        log.debug('')
        return PHFileWritter(**{
            'file_path': file_path or '',
            'file_content': file_content or [],
        })

    # SEARCHERS

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def search_client_by_alias(self, alias):
        log.debug('')
        registered_orbitals = self.fetch_hotel_orbitals()
        for orbital in registered_orbitals:
            if not orbital:
                registered_orbitals.remove(orbital)
                continue
            if orbital.fetch_alias() == alias:
                return orbital
        return False

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def search_chat_room_by_client_alias(self, client_alias):
        log.debug('')
        client = self.search_client_by_alias(client_alias)
        if not client:
            return self.warning_no_client_found_by_alias(
                client_alias, client
            )
        room_number = client.fetch_booked_room()
        floor_number = client.fetch_booked_floor()
        floor = self.search_floor_by_number(floor_number)
        if not floor:
            return self.warning_no_floor_found_by_number(
                floor_number, room_number,
            )
        room = floor.search_room_by_number(room_number)
        if not room:
            return self.warning_no_room_found_by_number(
                floor_number, room_number,
            )
        return room

    def search_chat_room_by_coordonates(self, floor_number, room_number):
        log.debug('')
        floor = self.search_floor_by_number(floor_number)
        if not floor:
            return self.warning_no_floor_found_by_number(
                floor_number, room_number,
            )
        room = floor.search_room_by_number(room_number)
        if not room:
            return self.warning_no_room_found_by_number(
                floor_number, room_number,
            )
        return room

    def search_floor_by_room_number(self, room_number, **kwargs):
        log.debug('')
        hotel_floors = self.fetch_hotel_floors()
        for floor in hotel_floors:
            if not hotel_floors[floor].search_room_by_number(room_number):
                continue
            return hotel_floors[floor]
        return self.warning_room_not_found_on_any_floor(
            room_number, list(hotel_floors.keys())
        )

    def search_room_by_number(self, room_number, **kwargs):
        log.debug('')
        hotel_floors = self.fetch_hotel_floors()
        for floor in hotel_floors:
            room = hotel_floors[floor].search_room_by_number(room_number)
            if not room:
                continue
            return room
        return self.warning_room_not_found_on_any_floor(
            room_number, list(hotel_floors.keys())
        )

    def search_floor_by_number(self, floor_number, **kwargs):
        log.debug('')
        hotel_floors = self.fetch_hotel_floors()
        if floor_number not in hotel_floors:
            return self.warning_hotel_floor_not_found(
                floor_number, list(hotel_floors.keys())
            )
        return hotel_floors[floor_number]

    # GENERAL

#   @pysnooper.snoop()
    def commit_floor_access_keys(self, floor_access_keys):
        log.debug('')
        hotel_floors = self.fetch_hotel_floors()
        success_count, failure_count, updated_floors = 0, 0, {}
        for floor_number in floor_access_keys:
            int_floor_number = int(floor_number)
            if int_floor_number not in hotel_floors:
                continue
            commit = hotel_floors[int_floor_number].set_access_key(
                floor_access_keys[floor_number]
            )
            if not commit:
                failure_count += 1
            else:
                updated_floors.update({
                    int_floor_number: hotel_floors[int_floor_number]
                })
                success_count += 1
        log.info(
            'Successfully set ({}) floor access keys, ({}) failures.'.format(
                success_count, failure_count
            )
        )
        return updated_floors

#   @pysnooper.snoop()
    def commit_level_access_keys_to_file(self, key_map):
        log.debug('')
        key_file = self.fetch_key_file()
        formatted_key_map = self.format_key_file_content_from_key_map(key_map)
        file_writter = self.fetch_state_writter()
        return file_writter.commit(target_file=key_file, content=formatted_key_map)

#   @pysnooper.snoop()
    def setup(self, **kwargs):
        log.debug('')
        hotel_floors = self.spawn_hotel_floors(floor_count=self.fetch_floor_count())
        if kwargs:
            floor_access_keys = kwargs
        else:
            floor_access_keys = self.generate_floor_access_keys()
        set_floor_access_keys = self.set_floor_access_keys(floor_access_keys)
        commit_access_keys = self.commit_floor_access_keys(floor_access_keys)
        store_access_keys = self.commit_level_access_keys_to_file(floor_access_keys)
        spawn_rooms = self.spawn_hotel_rooms(hotel_floors)
        state_map = self.build_state_map()
        set_state_map = self.set_state_map(state_map)
        ensure_files_exist = self.ensure_files_exist()
        commit_state = self.commit_server_state_to_file()
        return self.fetch_state_file()

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def checkout_room(self, client=None, floor_number=None,
                      room_number=None, **kwargs):
        log.debug('')
        if None in (client, floor_number, room_number):
            return self.error_invalid_checkout_instruction_values(
                client, room_number, kwargs
            )
        room = self.search_chat_room_by_coordonates(floor_number, room_number)
        if not room:
            return False
        checkout = room.client_checkout(client, **kwargs)
        if not checkout:
            return self.warning_could_not_checkout_client(
                client, floor_number, room_number, kwargs
            )
        floor = self.search_floor_by_number(room.fetch_floor_level())
        client = self.search_client_by_alias(client)
        floor_purge = floor.remove_orbital(client)
        hotel_purge = self.remove_orbital(client)
        commit_state = self.commit_server_state_to_file()
        return checkout

    def remove_orbital(self, orbital_user):
        log.debug('')
        if not isinstance(orbital_user, object) \
                or not orbital_user in self.hotel_orbitals:
            return self.error_invalid_orbital(orbital_user)
        self.hotel_orbitals.remove(orbital_user)
        self.update_timestamp()
        return self.hotel_orbitals

#   @pysnooper.snoop('logs/plaza-hotel.log')
    def join_room(self, guest=None, client=None, **kwargs):
        log.debug('')
        if None in (guest, client):
            return self.error_invalid_join_instruction_values(
                guest, client, kwargs
            )
        room = self.search_chat_room_by_client_alias(client)
        if not room:
            return False
        guest_join = room.guest_join(guest, **kwargs)
        if not guest_join:
            return self.warning_guest_could_not_join_room(
                guest, client, room, guest_join, kwargs
            )
        floor = self.search_floor_by_number(room.fetch_floor_level())
        floor_update = floor.update_orbitals(guest_join)
        hotel_update = self.update_orbitals(guest_join)
        commit_state = self.commit_server_state_to_file()
        return guest_join

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def checkin_room(self, client=None, floor_number=None,
                     room_number=None, **kwargs):
        log.debug('')
        if None in (client, floor_number, room_number):
            return self.error_invalid_checkin_instruction_values(
                client, floor_number, room_number, kwargs
            )
        room = self.search_chat_room_by_coordonates(floor_number, room_number)
        if not room:
            return False
        client_checkin = room.client_checkin(client, **kwargs)
        if not client_checkin:
            return self.warning_could_not_checkin_client(
                client_checkin, floor_number, room_number, kwargs
            )
        floor = self.search_floor_by_number(room.fetch_floor_level())
        floor_update = floor.update_orbitals(client_checkin)
        hotel_update = self.update_orbitals(client_checkin)
        commit_state = self.commit_server_state_to_file()
        return client_checkin

    def commit_server_state_to_file(self):
        log.debug('')
        state_map = self.build_state_map()
        set_State_map = self.set_state_map(state_map)
        state_file = self.fetch_state_file()
        formatted_state_map = self.format_state_file_content_from_state_map(state_map)
        file_writter = self.fetch_state_writter()
        return file_writter.commit(target_file=state_file, content=formatted_state_map)

#   @pysnooper.snoop()
    def spawn_hotel_rooms(self, hotel_floors=None):
        log.debug('')
        if not hotel_floors:
            hotel_floors = self.fetch_hotel_floors()
        room_count = self.fetch_room_count()
        floor_count = self.fetch_floor_count()
        total_room_count = floor_count * room_count
        current_room, floor_rooms, = 0, {}
        port_number = self.fetch_server_port_number()
        for floor_number in range(floor_count + 1):
            room_creation_values = []
            for room_number in range(room_count + 1):
                room_creation_values.append(
                    self.fetch_room_creation_values(
                        floor_level=floor_number, room_number=current_room,
                        port_number=port_number,
                    )
                )
                if room_number == room_count:
                    break
                current_room += 1
                port_number += 1
            floor_rooms.update({floor_number: room_creation_values})
        generated_rooms = []
        for floor_number in hotel_floors:
            if floor_number not in floor_rooms:
                self.warning_no_room_creation_values_generated_for_floor_level(
                    floor_number, floor_rooms.keys()
                )
                continue
            spawn_rooms = hotel_floors[floor_number].generate_rooms(
                floor_rooms[floor_number]
            )
            generated_rooms += spawn_rooms
        return generated_rooms

#   @pysnooper.snoop()
    def spawn_hotel_floors(self, floor_count=1):
        log.debug('')
        floor_values = [
            {'level': idx, 'log_name': log.name}
            for idx in range(floor_count + 1)
        ]
        new_floors = self.generate_hotel_floors(floor_values)
        return self.fetch_hotel_floors()

    # GENERATORS

    def generate_pseudorandom_sequence(self, length=36):
        log.debug('')
        character_set = string.ascii_lowercase + string.ascii_uppercase + string.digits
        return ''.join((random.choice(character_set) for i in range(length)))

    def generate_floor_access_keys(self):
        log.debug('')
        floor_count = self.fetch_floor_count()
        access_keys = {
            floor_number: self.generate_pseudorandom_sequence()
            for floor_number in range(1, floor_count + 1)
        }
        key_file_path = self.fetch_key_file()
        key_file_content = '\n'.join([
            '{} {}'.format(
                floor_number, access_keys[floor_number]
            ) for floor_number in access_keys
        ])
        with open(key_file_path, 'w') as fl:
            fl.write(key_file_content + '\n')
        return access_keys

#   @pysnooper.snoop()
    def generate_hotel_floors(self, floor_values):
        log.debug('')
        if not isinstance(floor_values, list):
            return self.error_invalid_floor_generator_value_set(floor_values)
        elif not floor_values:
            return self.error_no_floor_values_found(floor_values)
        new_floors = [
            self.create_hotel_floor(idx, **floor_values[idx])
            for idx in range(len(floor_values))
        ]
        self.update_floors({
            floor.fetch_level(): floor for floor in new_floors
        })
        return new_floors

    # ACTIONS

    def action_update_state_map_from_file(self):
        log.debug('')
        writter = self.fetch_state_writter()
        content = writter.load()
        state_map = self.format_state_map_from_state_file_content(content)
        self.ensure_state_from_map(state_map)
        return self.set_state_map(state_map)

    def action_update_state_file_from_map(self):
        log.debug('')
        state_map = self.build_state_map()
        content = self.format_state_file_content_from_state_map(state_map)
        writter = self.fetch_state_writter()
        writter.set_file_content(content)
        return writter.commit()

    # CLEANERS

    def cleanup_state_file(self):
        log.debug('')
        state_file = self.fetch_state_file()
        try:
            os.remove(state_file)
        except Exception as e:
            return self.warning_could_not_cleanup_state_file(
                state_file, e
            )
        return self.set_state_file(str())

    def cleanup_state_fifo(self):
        log.debug('')
        state_fifo = self.fetch_state_fifo()
        try:
            os.remove(state_fifo)
        except Exception as e:
            return self.warning_could_not_cleanup_state_fifo(
                state_fifo, e
            )
        return self.set_state_fifo(str())

    def cleanup_response_fifo(self):
        log.debug('')
        response_fifo = self.fetch_response_fifo()
        try:
            os.remove(response_fifo)
        except Exception as e:
            return self.warning_could_not_cleanup_response_fifo(
                response_fifo, e
            )
        return self.set_response_fifo(str())

    def cleanup(self):
        log.debug('')
        return {
            'state_file': self.cleanup_state_file(),
            'state_fifo': self.cleanup_state_fifo(),
            'response_fifo': self.cleanup_response_fifo(),
        }

    # DISPLAY

    def display_hotel_banner(self):
        log.debug('')
        print(
            '\n---[ Plaza Hotel ]--- Whisper Rendezvous --- ' \
            + datetime.datetime.now().strftime(
                self.timestamp_format
            ) + ' Last Update ---\n'
        )
        return True

    def display_hotel_map(self):
        log.debug('')
        self.update_hotel_map()
        return self.display_formatted_hotel_map()

#   @pysnooper.snoop()
    def display_formatted_hotel_map(self):
        log.debug('')
        hotel_map = self.fetch_hotel_map()
        self.display_hotel_banner()
        floor_access_keys = self.fetch_floor_access_keys()
        for floor_number in floor_access_keys:
            print(
                'Level', floor_number, 'Access Pass -', floor_access_keys[floor_number]
            )
        print('\n---[ Room Matrix ]--- FLOOR - [(ROOM, ORBITAL, PORT, GUESTS), ...]\n')
        for floor_level in range(len(hotel_map)):
            print(
                'Floor', len(hotel_map) - 1 - floor_level, '-',
                hotel_map[len(hotel_map) - 1 - floor_level]
            )
        return True

    # OVERRIDES

    def __str__(self, *args, **kwargs):
        log.debug('')
        return self.format_hotel_detail_string()

    # WARNINGS

    def warning_no_key_file_content_formatted(self, *args):
        log.warning('No key file content could be formatted. Details: {}'.format(args))
        return False

    def warning_malformed_state_file_room_line(self, *args):
        log.warning('Malformed state file room line. Details: {}'.format(args))
        return False

    def warning_malformed_state_file_floor_line(self, *args):
        log.warning('Malformed state file floor line. Details: {}'.format(args))
        return False

    def warning_malformed_state_file_client_line(self, *args):
        log.warning('Malformed state file client line. Details: {}'.format(args))
        return False

    def warning_malformed_state_file_guest_line(self, *args):
        log.warning('Malformed state file guest line. Details: {}'.format(args))
        return False

    def warning_guest_could_not_join_room(self, *args):
        log.warning('Guest could jot join room. Details: {}'.format(args))
        return False

    def warning_no_client_found_by_alias(self, *args):
        log.warning('No client found by alias. Details: {}'.format(args))
        return False

    def warning_could_not_checkout_client(self, *args):
        log.warning('Could not check-out client. Details: {}'.format(args))
        return False

    def warning_room_not_found_on_any_floor(self, *args):
        log.warning('Room not found on any floor. Details: {}'.format(args))
        return False

    def warning_could_not_checkin_client(self, *args):
        log.warning('Could not check-in client. Details: {}'.format(args))
        return False

    def warning_no_room_found_by_number(self, *args):
        log.warning('No room found by number. Details: {}'.format(args))
        return False

    def warning_no_floor_found_by_number(self, *args):
        log.warning('No floor found by number. Details: {}'.format(args))
        return False

    def warning_hotel_floor_not_found(self, *args):
        log.warning('Hotel floor not found. Details: {}'.format(args))
        return False

    def warning_could_not_cleanup_response_fifo(self, *args):
        log.warning(
            'Something went wrong. '
            'Could not cleanup response fifo. '
            'Details: {}'.format(args)
        )
        return False

    def warning_could_not_cleanup_state_fifo(self, *args):
        log.warning(
            'Something went wrong. '
            'Could not cleanup state fifo. '
            'Details: {}'.format(args)
        )
        return False

    def warning_could_not_cleanup_state_file(self, *args):
        log.warning(
            'Something went wrong. '
            'Could not cleanup state file. '
            'Details: {}'.format(args)
        )
        return False

    def warning_no_room_creation_values_generated_for_floor_level(self, *args):
        log.warning(
            'Something went wrong. '
            'No room creation values generated for floor level. '
            'Details: {}'.format(args)
        )
        return False

    def warning_room_not_found(self, *args):
        log.warning('Room not found. Details: {}'.format(args))
        return False

    def warning_floor_not_found(self, *args):
        log.warning('Floor not found. Details: {}'.format(args))
        return False

    # ERRORS

    def error_invalid_level_access_key_map(self, *args):
        log.error('Invalid level access key. Details: {}'.format(args))
        return False

    def error_invalid_orbital(self, *args):
        log.error('Invalid orbital user. Details: {}'.format(args))
        return False

    def error_invalid_join_instruction_values(self, *args):
        log.error('Invalid join instruction values. Details: {}'.format(args))
        return False

    def error_invalid_checkout_instruction_values(self, *args):
        log.error('Invalid checkout instruction values. Details: {}'.format(args))
        return False

    def error_could_not_ensure_fifo_exists(self, *args):
        log.error(
            'Something went wrong. '
            'Could not ensure fifo exists. '
            'Details: {}'.format(args)
        )
        return False

    def error_could_not_ensure_text_file_exists(self, *args):
        log.error(
            'Something went wrong. '
            'Could not ensure text file exists. '
            'Details: {}'.format(args)
        )
        return False

    def error_invalid_checkin_instruction_values(self, *args):
        log.error('Invalid checkin instruction values. Details: {}'.format(args))
        return False

    def error_invalid_floor_access_keys(self, *args):
        log.error('Invalid hotel floor access keys. Details: {}'.format(args))
        return False

    def error_invalid_hotel_room_count(self, *args):
        log.error('Invalid hotel room count. Details: {}'.format(args))
        return False

    def error_invalid_hotel_floor_count(self, *args):
        log.error('Invalid hotel floor count. Details: {}'.format(args))
        return False

    def error_no_floor_values_found(self, *args):
        log.error('No floor creation values found. Details: {}'.format(args))
        return False

    def error_invalid_floor_generator_value_set(self, *args):
        log.error('Invalid floor generator value set. Details: {}'.format(args))
        return False

    def error_invalid_floor_level(self, *args):
        log.error('Invalid hotel floor level. Details: {}'.format(args))
        return False

    def error_invalid_hotel_map(self, *args):
        log.error('Invalid hotel map. Details: {}'.format(args))
        return False

    # CODE DUMP


