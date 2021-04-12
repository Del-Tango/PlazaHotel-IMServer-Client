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


class PHGuest(PHUser):

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        res = super().__init__(category='guest', *args, **kwargs)
        self.guest_of = kwargs.get('guest_of', str())
        self.room_number = kwargs.get('room_number', int())
        self.floor_number = kwargs.get('floor_number', int())
        self.access_key = kwargs.get('access_key', int())
        return res

    # FETCHERS

    def fetch_details(self):
        log.debug('')
        return {
            'alias': self.alias,
            'guest_of': self.guest_of,
            'room_number': self.room_number,
            'floor_number': self.floor_number,
            'access_key': self.access_key,
            'allowed_floors': self.allowed_floors,
            'allowed_rooms': self.allowed_rooms,
            'timestamp': self.timestamp.strftime(self.fetch_timestamp_format())
        }
