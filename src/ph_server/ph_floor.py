#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# HOTEL

import logging
import pysnooper
import datetime

from .ph_room import PHRoom
from .ph_client import PHClient

log = logging.getLogger(__name__)


class PHFloor(object):

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        self.level = kwargs.get('level', int())
        self.rooms = kwargs.get('room', dict())
        self.orbitals = kwargs.get('orbitals', list())
        self.timestamp = datetime.datetime.now()
        self.room_count = len(self.rooms)
        self.user_count = len(self.orbitals)
        self.access_key = kwargs.get('access_key', str())
        self.timestamp_format = kwargs.get('timestamp_formt', '%d/%m/%Y-%H:%M:%S')

    # FETCHERS

    def fetch_timestamp_format(self):
        log.debug('')
        return self.timestamp_format

    def fetch_access_key(self):
        log.debug('')
        return self.access_key

    def fetch_floor_details(self):
        log.debug('')
        return {
            'level': self.level,
            'rooms': self.rooms,
            'orbitals': self.orbitals,
            'timestamp': self.timestamp.strftime(self.fetch_timestamp_format()),
            'room_count': self.room_count,
            'user_count': self.user_count,
            'log_name': log.name,
            'access_key': self.access_key,
        }

    def fetch_level(self):
        log.debug('')
        return self.level

    def fetch_rooms(self):
        log.debug('')
        return self.rooms

    def fetch_orbitals(self):
        log.debug('')
        return self.orbitals

    def fetch_room_count(self):
        log.debug('')
        return self.room_count

    def fetch_user_count(self):
        log.debug('')
        return self.user_count

    def fetch_timestamp(self):
        log.debug('')
        return self.timestamp

    # SETTERS

    def set_access_key(self, access_key):
        log.debug('')
        self.access_key = access_key
        self.update_timestamp()
        return self.access_key

    def set_room_count(self, room_count):
        log.debug('')
        self.room_count = room_count
        self.update_timestamp()
        return self.room_count

    def set_user_count(self, user_count):
        log.debug('')
        self.user_count = user_count
        self.update_timestamp()
        return self.user_count

    def set_timestamp(self, timestamp):
        log.debug('')
        self.timestamp = timestamp
        return self.timestamp

    def set_level(self, level):
        log.debug('')
        self.level = level
        self.update_timestamp()
        return self.level

    def set_rooms(self, rooms):
        log.debug('')
        self.rooms = rooms
        self.update_room_count()
        self.update_timestamp()
        return self.rooms

    def set_orbitals(self, orbitals):
        log.debug('')
        self.orbitals = orbitals
        self.update_timestamp()
        return self.orbitals

    # CHECKERS

    def check_has_room(self, room_number):
        log.debug('')
        return room_number in self.fetch_rooms()

    def check_access_key(self, access_key=None):
        log.debug('')
        valid_key = self.fetch_access_key()
        if valid_key == '':
            return True
        elif not access_key or not isinstance(access_key, str):
            return self.error_invalid_access_key(access_key)
        return valid_key == access_key

    # UPDATERS

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def update_user_count(self):
        log.debug('')
        user_count, orbitals, hotel_rooms = 0, [], self.fetch_rooms()
        for room_number in hotel_rooms:
            client = hotel_rooms[room_number].fetch_client()
            if client:
                orbitals.append(client)
                user_count += 1
            guests = hotel_rooms[room_number].fetch_guests()
            orbitals += guests
            user_count += len(guests)
        self.set_orbitals(orbitals)
        return self.set_user_count(user_count)

    def update_timestasmp(self):
        log.debug('')
        return self.set_timestamp(datetime.datetime.now())

    def update_room_count(self):
        log.debug('')
        return self.set_room_count(len(self.fetch_rooms()))

    def update_timestamp(self):
        log.debug('')
        return self.set_timestamp(datetime.datetime.now())

    def update_rooms(self, room_map):
        log.debug('')
        if not isinstance(room_map, dict):
            return self.error_invalid_room_map(room_map)
        self.rooms.update(room_map)
        self.update_room_count()
        return self.rooms

    def update_orbitals(self, orbital):
        log.debug('')
        if not isinstance(orbital, object):
            return self.error_invalid_orbital(orbital)
        self.orbitals.append(orbital)
        self.update_user_count()
        return self.orbitals

    # CREATORS

#   @pysnooper.snoop()
    def create_room(self, creation_values):
        log.debug('')
        try:
            room = PHRoom(**creation_values)
        except Exception as e:
            return self.error_could_not_create_room(creation_values, e)
        return room

    # FORMATTERS

    def format_floor_detail_string(self):
        log.debug('')
        details = '<(Floor)- Level: {}, Room Count: {}, Orbital Count: {}, Access Key: {}>'\
            .format(
                self.level, self.room_count, self.user_count, self.access_key
            )
        return details

    # SEARCHERS

    def search_room_by_number(self, room_number):
        log.debug('Level ({})'.format(self.level))
        if not isinstance(room_number, int):
            return self.error_invalid_room_number(room_number)
        rooms = self.fetch_rooms()
        if not rooms:
            return self.error_no_rooms_found_on_floor(room_number, rooms)
        elif room_number not in rooms:
            return self.warning_room_not_found(room_number, rooms)
        return rooms[room_number]

    # OVERRIDES

    def __str__(self, *args, **kwargs):
        log.debug('')
        return self.format_floor_detail_string()

    # GENERAL

#   @pysnooper.snoop('../logs/plaza-hotel.log')
    def remove_orbital(self, orbital):
        log.debug('')
        if not isinstance(orbital, object) or orbital not in self.orbitals:
            return self.error_invalid_orbital(orbital)
        self.orbitals.remove(orbital)
        self.update_user_count()
        return self.orbitals

    # GENERATORS

#   @pysnooper.snoop()
    def generate_rooms(self, room_values):
        log.debug('')
        if not isinstance(room_values, list):
            return self.error_invalid_room_generator_value_set(room_values)
        elif not len(room_values):
            return self.error_no_room_values_found(room_values)
        new_rooms = [
            self.create_room(room_values[idx])
            for idx in range(len(room_values) - 1)
        ]
        self.update_rooms({
            room.fetch_room_number(): room for room in new_rooms
        })
        return new_rooms

    # CLEANERS

    def cleanup(self):
        log.debug('')
        self.level = str()
        self.rooms = dict()
        self.orbitals = list()
        self.timestamp = datetime.datetime.now()
        self.room_count = len(self.rooms)
        self.user_count = len(self.orbitals)
        return True

    # WARNINGS

    def warning_room_not_found(self, *args):
        log.warning(
            'Room not found. Details: {}'.format(args)
        )
        return False

    # ERRORS

    def error_invalid_room_number(self, *args):
        log.error(
            'Invalid room number. Details: {}'.format(args)
        )
        return False

    def error_no_rooms_found_on_floor(self, *args):
        log.error(
            'No rooms found on specified floor. Details: {}'.format(args)
        )
        return False

    def error_invalid_access_key(self, *args):
        log.error(
            'Invalid access key. Details: {}'.format(args)
        )
        return False

    def error_could_not_create_room(self, *args):
        log.error(
            'Something went wrong. '
            'Could not create room on floor {}. '
            'Details: {}'.format(self.level, args)
        )
        return False

    def error_no_room_values_found(self, *args):
        log.error(
            'No room creation values found. Details: {}'.format(args)
        )
        return False

    def error_invalid_room_generator_value_set(self, *args):
        log.error(
            'Invalid room generator value set. Details: {}'.format(args)
        )
        return False

    def error_invalid_orbital(self, *args):
        log.error(
            'Invalid orbital. Details: {}'.format(args)
        )
        return False

    def error_invalid_room_map(self, *args):
        log.error(
            'Invalid room map. Details: {}'.format(args)
        )
        return False


