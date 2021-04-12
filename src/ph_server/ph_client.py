#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# CLIENT

import os
import datetime
import sys
import logging
import pysnooper

from .ph_user import PHUser

log = logging.getLogger(__name__)


class PHClient(PHUser):

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        res = super().__init__(category='client', *args, **kwargs)
        self.booked_floor = kwargs.get('booked_floor', int())
        self.booked_room = kwargs.get('booked_room', int())
        self.guest_limit = kwargs.get('guest_limit', int())
        return res

    # FETCHERS

    def fetch_booked_floor(self):
        log.debug('')
        return self.booked_floor

    def fetch_booked_room(self):
        log.debug('')
        return self.booked_room

    def fetch_guest_limit(self):
        log.debug('')
        return self.guest_limit

    def fetch_values(self):
        log.debug('')
        res = super().fetch_values()
        res.update({
            'booked_floor': self.booked_floor,
            'booked_room': self.booked_room,
            'guest_limit': self.guest_limit,
        })
        return res

    # SETTERS

    def set_booked_floor(self, floor_number):
        log.debug('')
        if not isinstance(floor_number, int):
            return self.error_invalid_floor_number(floor_number)
        self.booked_floor = floor_number
        self.update_timestamp()
        return self.booked_floor

    def set_booked_room(self, room_number):
        log.debug('')
        if not isinstance(room_number, int):
            return self.error_invalid_room_number(room_number)
        self.booked_room = room_number
        self.update_timestamp()
        return self.booked_room

    def set_guest_limit(self, number_of_guests):
        log.debug('')
        if not isinstance(number_of_guests, int):
            return self.error_invalid_guest_limit(number_of_guests)
        self.guest_limit = number_of_guests
        self.update_timestamp()
        return self.guest_limit

    # CHECKERS

    def check_floor_access_key(self, access_key):
        log.debug('')
        if not isinstance(access_key, str):
            return self.error_invalid_floor_access_key(access_key)
        return self.fetch_floor_access_key() == access_key

    # CLEANERS

    def cleanup(self):
        res = super().cleanup()
        self.set_floor_access_key(self, str())
        self.set_booked_floor(self, int())
        self.set_booked_room(self, int())
        self.set_guest_limit(self, int())
        return self.fetch_values()

    # ERRORS

    def error_invalid_guest_limit(self, *args):
        log.error('Invalid guest limit. Details: {}'.format(args))
        return False

    def error_invalid_room_number(self, *args):
        log.error('Invalid room number. Details: {}'.format(args))
        return False

    def error_invalid_floor_number(self, *args):
        log.error('Invalid floor number. Details: {}'.format(args))
        return False

    def error_invalid_floor_access_key(self, *args):
        log.error('Invalid floor access key. Details: {}'.format(args))
        return False


if __name__ == '__main__':
    client = PHClient(**{
        'alias': 'TestClient',
        'booked_floor': 4,
        'booked_room': 1,
        'guest_limit': 20,
        'allowed_rooms': [1, 2, 3],
        'allowed_floors': [0, 1, 2, 3, 4],
        'superuser_flag': True,
    })
    print(client)
    print(client.fetch_values())
