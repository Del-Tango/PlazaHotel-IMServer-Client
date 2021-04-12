#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# FIFO PIPE WRITTER

import os
import sys
import logging
import pysnooper
import time
import optparse

from ph_server.ph_fifo_writter import PHFifoWritter

# HOT PARAMETERS

SCRIPT_NAME = 'PH-PipeWritter'
TIMESTAMP_FORMAT = '%d/%m/%Y-%H:%M:%S'
LOG_FILE_PATH='logs/plaza-hotel.log'
LOG_FORMAT = '[ %(asctime)s ] %(name)s [ %(levelname)s ] %(thread)s - '\
    '%(filename)s - %(lineno)d: %(funcName)s - %(message)s'
SILENT = 'off' # (on | off)
FIFO_PATH = '/tmp/phs.fifo'
MESSAGE = '.update'

# COLD PARAMETERS

FIFO_WRITTER = None

# LOGGING

#@pysnooper.snoop()
def log_init(log_name=__name__):
    log = logging.getLogger(log_name)
    try:
        log.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(LOG_FILE_PATH, 'a')
        formatter = logging.Formatter(LOG_FORMAT, TIMESTAMP_FORMAT)
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
    finally:
        return log

log = log_init(SCRIPT_NAME)

# FETCHERS

def fetch_fifo_writter_creation_values(**kwargs):
    log.debug('')
    creation_values = {
        'fifo': kwargs.get('fifo', FIFO_PATH),
        'log_name': kwargs.get('log_name', SCRIPT_NAME),
    }
    return creation_values

# CREATORS

def create_fifo_writter(**kwargs):
    log.debug('')
    creation_values = fetch_fifo_writter_creation_values(**kwargs)
    fifo_writter = PHFifoWritter(**creation_values)
    return fifo_writter

def create_command_line_parser():
    log.debug('')
    parser = optparse.OptionParser(
        ' %prog \ \n'
        '   -h | --help \ \n'
        '   -f | --fifo-path=/path/to/named/pipe \ \n'
        '   -m | --message="Message to write" \ \n'
        '   -s | --silent=(on | off) \ \n'
        '   -l | --log-file=/path/to/log/file '
    )
    return parser

# DISPLAY

def display_pipe_writter_banner():
    log.debug('')
    banner = '\n________________________________________________________________________________\n\n'\
        '  *                    *   Plaza Hotel - Pipe Writter   *                    *  \n'\
        '________________________________________________________________________________\n'\
        '                     Regards, the Alveare Solutions society.\n'
    return stdout_msg(banner)

# PROCESSORS

def process_command_line_options(parser):
    log.debug('')
    (options, args) = parser.parse_args()
    # [ NOTE ]: If you trully want to be covert, process silent_flag first
    processed = {
        'silent_flag': process_silent_flag_argument(parser, options),
        'fifo_path': process_fifo_path_argument(parser, options),
        'message': process_message_argument(parser, options),
        'log_file': process_log_file_argument(parser, options),
    }
    return processed

def process_silent_flag_argument(parser, options):
    global SILENT
    log.debug('')
    silent_flag = options.silent_flag
    if not silent_flag:
        log.warning(
            'No silent flag provided. '
            'Defaulting to ({}).'.format(SILENT)
        )
        return False
    SILENT = silent_flag
    stdout_msg(
        '[ + ]: Silent flag setup ({}).'.format(SILENT)
    )
    return True

def process_fifo_path_argument(parser, options):
    global FIFO_PATH
    log.debug('')
    fifo_path = options.fifo_path
    if not fifo_path:
        log.warning(
            'No named pipe path provided. '
            'Defaulting to ({}).'.format(FIFO_PATH)
        )
        return False
    FIFO_PATH = fifo_path
    stdout_msg(
        '[ + ]: Named pipe setup ({}).'.format(FIFO_PATH)
    )
    return True

def process_message_argument(parser, options):
    global MESSAGE
    log.debug('')
    message = options.message
    if not message:
        log.warning(
            'No message provided. '
            'Defaulting to ({}).'.format(MESSAGE)
        )
        return False
    MESSAGE = message
    stdout_msg(
        '[ + ]: Message setup ({}).'.format(MESSAGE)
    )
    return True

def process_log_file_argument(parser, options):
    global LOG_FILE_PATH
    log.debug('')
    file_path = options.log_file
    if not file_path:
        log.warning(
            'No log file path provided. '
            'Defaulting to ({}).'.format(LOG_FILE_PATH)
        )
        return False
    LOG_FILE_PATH = file_path
    stdout_msg(
        '[ + ]: Log file setup ({}).'.format(LOG_FILE_PATH)
    )
    return True

# GENERAL

def setup_fifo_pipe_writter(fifo_path):
    global FIFO_WRITTER
    log.debug('')
    FIFO_WRITTER = create_fifo_writter(fifo=fifo_path)
    return FIFO_WRITTER

def write_to_fifo_pipe(message):
    log.debug('')
    return FIFO_WRITTER.write(content=message)

def add_command_line_parser_options(parser):
    log.debug('')
    parser.add_option(
        '-f', '--fifo-path', dest='fifo_path', type='string',
        help='Fifo Pipe Path - Path to named pipe.',
        metavar='FIFO'
    )
    parser.add_option(
        '-m', '--message', dest='message', type='string',
        help='Message - Message to write to named pipe.',
        metavar='MSG'
    )
    parser.add_option(
        '-s', '--silent', dest='silent_flag', type='string',
        help='Silent - Silence STDOUT messages.',
        metavar='(on | off)'
    )
    parser.add_option(
        '-l', '--log-file', dest='log_file', type='string',
        help='Log File - File to log messages to.',
        metavar='FILE'
    )
    return parser

def stdout_msg(message):
    log.debug('')
    log.info(message)
    if SILENT == 'off':
        print(message)
        return True
    return False

#@pysnooper.snoop()
def parse_command_line_arguments():
    log.debug('')
    parser = create_command_line_parser()
    add_parser_options = add_command_line_parser_options(parser)
    return process_command_line_options(parser)

# MISCELLANEOUS

if __name__ == '__main__':
    parse_command_line_arguments()
    display_pipe_writter_banner()
    try:
        setup_fifo_pipe_writter(FIFO_PATH)
        write_to_fifo_pipe(MESSAGE)
    except Exception as e:
        exit(1)
    exit(0)


