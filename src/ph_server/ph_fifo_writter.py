#!/usr/bin/python3

import os
import sys
import logging
import pysnooper

log = logging.getLogger(__name__)


class PHFifoWritter():

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        self.fifo = kwargs.get('fifo', '')

    def __str__(self):
        log.debug('')
        return '<PHFifoWritter-(' + self.fifo + ')>'

    # FETCHERS

    def fetch_fifo_path(self):
        log.debug('')
        return self.fifo

    # SETTERS

    def set_fifo_path(self, fifo_path):
        log.debug('')
        self.fifo = fifo_path
        return self.fifo

    # GENERAL

#   @pysnooper.snoop()
    def write(self, filename=None, content=None):
        log.debug('')
        if not content:
            return self.warning_no_content_to_write()
        filename = filename or self.fetch_fifo_path()
        try:
            log.info('Writting ({}) to ({})'.format(content, filename))
            with open(filename, 'w') as fifo:
                fifo.write(content)
        except Exception as e:
            log.error(e)
            return False
        return True

#   @pysnooper.snoop()
    def read(self, filename=None):
        log.debug('')
        filename = filename or self.fetch_fifo_path()
        log.info('Reading fifo ({}),'.format(filename))
        while True:
            with open(filename, 'r') as fifo:
                content = fifo.read()
                log.info('Fifo content ({})'.format(content))
                yield content

    def cleanup(self):
        log.debug('')
        fifo_path = self.fetch_fifo_path()
        try:
            os.unlink(fifo_path)
        except Exception as e:
            return self.error_could_not_cleanup_fifo(fifo_path, e)
        return True

#   @pysnooper.snoop()
    def setup(self):
        log.debug('')
        fifo_path = self.fetch_fifo_path()
        try:
            os.mkfifo(fifo_path)
        except Exception as e:
            return self.error_could_not_setup_fifo(fifo_path, e)
        return True

    # WARNINGS

    def warning_no_content_to_write(self, *args):
        log.warning('No content specified to write. Details: {}'.format(args))
        return False

    # ERRORS

    def error_could_not_setup_fifo(self, *args):
        log.error(
            'Something went wrong. '
            'Could not setup FIFO. '
            'Details: {}'.format(args)
        )
        return False

    def error_could_not_cleanup_fifo(self, *args):
        log.error(
            'Something went wrong. '
            'Could not cleanup FIFO. '
            'Details: {}'.format(args)
        )
        return False


