#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# USER

import os
import datetime
import sys
import logging
import pysnooper

log = logging.getLogger(__name__)


class PHUser(object):

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        self.alias = kwargs.get('alias', 'You')
        self.superuser_flag = kwargs.get('superuser_flag', True)
        self.allowed_floors = kwargs.get('allowed_floors', [])
        self.allowed_rooms = kwargs.get('allowed_rooms', [])
        self.category = kwargs.get('category', 'user')
        self.access_key = kwargs.get('access_key', '')
        self.timestamp_format = kwargs.get('timestamp_format', '%d/%m/%Y-%H:%M:%S')
        self.timestamp = datetime.datetime.now()

    # FETCHERS

    def fetch_timestamp_format(self):
        log.debug('')
        return self.timestamp_format

    def fetch_access_key(self):
        log.debug('')
        return self.access_key

    def fetch_category(self):
        log.debug('')
        return self.category

    def fetch_alias(self):
        log.debug('')
        return self.alias

    def fetch_superuser_flag(self):
        log.debug('')
        return self.superuser_flag

    def fetch_allowed_floors(self):
        log.debug('')
        return self.allowed_floors

    def fetch_allowed_rooms(self):
        log.debug('')
        return self.allowed_rooms

    def fetch_values(self):
        log.debug('')
        return {
            'alias': self.alias,
            'superuser_flag': self.superuser_flag,
            'allowed_floors': self.allowed_floors,
            'allowed_rooms': self.allowed_rooms,
            'timestamp': self.timestamp.strftime(self.fetch_timestamp_format())
        }

    def fetch_supported_category_labels(self):
        log.debug('')
        return ('user', 'client', 'guest')

    # SETTERS

    def set_timestamp(self, timestamp):
        log.debug('')
        self.timestamp = timestamp
        return self.timestamp

    def set_access_key(self, access_key):
        log.debug('')
        if not isinstance(access_key, str):
            return self.error_invalid_access_key(access_key)
        self.access_key = access_key
        self.update_timestamp()
        return self.access_key

    def set_category(self, category_label):
        log.debug('')
        if category_label not in self.fetch_supported_category_labels():
            return self.error_invalid_category_label(category_label)
        self.category = category_label
        self.update_timestamp()
        return self.category

    def set_alias(self, alias):
        log.debug('')
        if not isinstance(alias, str):
            return self.error_invalid_alias(alias)
        self.alias = alias
        self.update_timestamp()
        return self.alias

    def set_superuser_flag(self, flag):
        log.debug('')
        if not isinstance(flag, bool):
            return self.error_invalid_superuser_flag(flag)
        self.superuser_flag = flag
        self.update_timestamp()
        return self.superuser_flag

    def set_allowed_floors(self, floor_numbers):
        log.debug('')
        if not isinstance(floor_numbers, list):
            return self.error_invalid_floor_numbers(floor_numbers)
        self.allowed_floors = floor_numbers
        self.update_timestamp()
        return self.allowed_floors

    def set_allowed_rooms(self, room_numbers):
        log.debug('')
        if not isinstance(room_numbers, list):
            return self.error_invalid_room_numbers(room_numbers)
        self.allowed_rooms = room_numbers
        self.update_timestamp()
        return self.allowed_rooms

    # UPDATERS

    def update_timestamp(self):
        log.debug('')
        return self.set_timestamp(datetime.datetime.now())

    def update_allowed_floors(self, floor_numbers):
        log.debug('')
        self.allowed_floors += floor_numbers
        self.update_timestamp()
        return self.allowed_floors

    def update_allowed_rooms(self, room_numbers):
        log.debug('')
        self.allowed_rooms += room_numbers
        self.update_timestamp()
        return self.allowed_rooms

    # CHECKERS

    def is_client(self):
        log.debug('')
        return self.fetch_category() == 'client'

    def is_guest(self):
        log.debug('')
        return self.fetch_category() == 'guest'

    def is_superuser(self):
        log.debug('')
        return self.fetch_superuser_flag()

    # CLEANERS

    def cleanup(self):
        self.set_alias('')
        self.set_superuser_flag(False)
        self.set_allowed_rooms([])
        self.set_allowed_floors([])
        return self.fetch_values()

    # FORMATTERS

    def format_user_details(self):
        log.debug('')
        details = 'User {} - Super User: {}, Floor Access: {}, Room Access: {}'\
            .format(
                self.alias, self.superuser_flag, self.allowed_floors,
                self.allowed_rooms
            )
        return details

    # DUNDER

    def __str__(self, *args, **kwargs):
        return self.format_user_details()

    # ERRORS

    def error_invalid_access_key(self, *args):
        log.error('Invalid floor access key. Details: {}'.format(args))
        return False

    def error_invalid_category_label(self, *args):
        log.error('Invalid category label. Details: {}'.format(args))
        return False

    def error_invalid_floor_numbers(self, *args):
        log.error('Invalid floor numbers. Details: {}'.format(args))
        return False

    def error_invalid_room_numbers(self, *args):
        log.error('Invalid room numbers. Details: {}'.format(args))
        return False

    def error_invalid_superuser_flag(self, *args):
        log.error('Invalid superuser flag. Details: {}'.format(args))
        return False

    def error_invalid_alias(self, *args):
        log.error('Invalid alias. Details: {}'.format(args))
        return False

if __name__ == '__main__':
    user = PHUser(**{
        'alias': 'TestClient',
        'allowed_rooms': [1, 2, 3],
        'allowed_floors': [0, 1, 2, 3, 4],
        'superuser_flag': True,
    })
    print(user)
    print(user.fetch_values())
