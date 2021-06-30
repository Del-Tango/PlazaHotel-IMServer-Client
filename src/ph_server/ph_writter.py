#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# FILE WRITTER

import os
import sys
import datetime
import pysnooper
import logging

log = logging.getLogger(__name__)


class PHFileWritter():

    def __init__(self, *args, **kwargs):
        global log
        log = logging.getLogger(kwargs.get('log_name', __name__))
        log.debug('')
        self.file_path = kwargs.get('file_path', str())
        self.file_content = kwargs.get('file_content', list())

    # FETCHERS

    def fetch_file_path(self):
        log.debug('')
        return self.file_path

    def fetch_file_content(self):
        log.debug('')
        return self.file_content

    # SETTERS

    def set_file_path(self, file_path):
        log.debug('')
        if not self.check_file_exists(file_path):
            return self.error_file_not_found(file_path)
        self.file_path = file_path
        return self.file_path

    def set_file_content(self, file_content):
        log.debug('')
        if not self.isinstance(file_content, list):
            return self.error_invalid_file_content_cache(file_content)
        self.file_content = file_content
        return self.file_content

    # CHECKERS

    def check_file_exists(self, file_path):
        log.debug('')
        return os.path.isfile(file_path)

    # UPDATERS

    def update_file_content_cache(self, file_content):
        log.debug('')
        if not self.isinstance(file_content, list):
            return self.error_invalid_file_content_cache(file_content)
        self.file_content += file_content
        return self.file_content

    # GENERAL

#   @pysnooper.snoop()
    def commit(self, target_file=None, content=None):
        '''
        [ NOTE ]: Writtes the string found in the file_content variable to file/
        '''
        log.debug('')
        target_file = target_file or self.fetch_file_path()
        if not target_file:
            return self.warning_could_not_fetch_target_file(target_file, content)
        elif not self.check_file_exists(target_file):
            return self.error_file_not_found(target_file)
        content = content or self.fetch_file_content()
        with open(target_file, 'w') as target_stream:
            target_stream.write('\n'.join(content) + '\n')
        return target_file

    def read(self, target_file=None):
        '''
        [ NOTE ]: Returns the file content without modifying the file_content variable
        '''
        log.debug('')
        target_file = target_file or self.fetch_file_path()
        if not target_file:
            return self.warning_could_not_fetch_target_file(target_file)
        elif not self.check_file_exists(target_file):
            return self.error_file_not_found(target_file)
        content = []
        with open(target_file, 'r') as target_stream:
            content = target_stream.readlines()
        if content == []:
            self.warning_target_file_empty(target_file, content)
        return content

    def load(self, target_file=None):
        '''
        [ NOTE ]: Modifies the file_content variable with data read from the file.
        '''
        log.debug('')
        target_file = target_file or self.fetch_file_path()
        if not target_file:
            return self.warning_could_not_fetch_target_file(target_file)
        elif not self.check_file_exists(target_file):
            return self.error_file_not_found(target_file)
        content = []
        with open(target_file, 'r') as target_stream:
            content = target_stream.readlines()
        if content == []:
            self.warning_target_file_empty(target_file, content)
        self.set_file_content(content)
        return content

    def update(self, file_content, target_file=None):
        '''
        [ NOTE ]: Append information to the file
        '''
        log.debug('')
        target_file = target_file or self.fetch_file_path()
        if not target_file:
            return self.warning_could_not_fetch_target_file(target_file)
        elif not self.check_file_exists(target_file):
            return self.error_file_not_found(target_file)
        content = self.read(target_file)
        content += file_content
        return self.commit(target_file=target_file, file_content=content)

    # WARNINGS

    def warning_target_file_empty(self, *args):
        log.warning('Target file empty. Details: {}'.format(args))
        return False

    def warning_could_not_fetch_target_file(self, *args):
        log.warning(
            'Something went wrong. '
            'Could not fetch target file. '
            'Details: {}'.format(args)
        )
        return False

    # ERRORS

    def error_invalid_file_content_cache(self, *args):
        log.error('Invalid file content cache. Details: {}'.format(args))
        return False

    def error_file_not_found(self, *args):
        log.error('File not found. Details: {}'.format(args))
        return False


if __name__ == '__main__':
    writter = PHFileWritter(
        file_path='/tmp/pf-file-writter.tmp',
        file_content=['This is the first line.', 'This is the second'],
    )
    writter.commit()
    print(writter.read())

