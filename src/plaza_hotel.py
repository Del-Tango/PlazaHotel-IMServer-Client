#!/usr/bin/python3
#
# Regards, the Alveare Solutions society.
#
# PLAZA HOTEL (v.Whispers)

import os
import logging
import time
import threading
import optparse
import pathlib
import pysnooper

from ph_client.ph_chat_client import PHChatClient
from ph_server.ph_hotel import PHHotel
from ph_server.ph_fifo_writter import PHFifoWritter
from ph_server.ph_writter import PHFileWritter

# HOT PARAMETERS

SCRIPT_NAME = 'PlazaHotel'
VERSION = 'v.Whispers'
VERSION_NUMBER = '1.0'
RUNNING_MODE = 'client' # (server | client)
TIMESTAMP_FORMAT = '%d/%m/%Y-%H:%M:%S'
CURRENT_DIRECTORY = str(pathlib.Path(__file__).parent.absolute())
LOG_FILE_PATH = CURRENT_DIRECTORY + '/logs/plaza-hotel.log'
LOG_FORMAT = '[ %(asctime)s ] %(name)s [ %(levelname)s ] %(thread)s - '\
    '%(filename)s - %(lineno)d: %(funcName)s - %(message)s'

# Server Specific
FLOOR_COUNT = 3
ROOM_COUNT = 3
CAPACITY = 20
BUFFER_SIZE = 4096
SILENT = 'off' # (on | off)
STATE_FILE = '/tmp/phs.tmp'
KEY_FILE = '/tmp/phk.tmp'
STATIC_KEY_FILE='/tmp/phk.tmp'
STATE_FIFO = '/tmp/phs.fifo'
RESPONSE_FIFO = '/tmp/phr.fifo'
FILE_PERMISSIONS = 750

# Client Specific
CLIENT_TYPE='client'    # (client | guest)
PORT_NUMBER = 3000
ADDRESS = '127.0.0.1'
ALIAS = 'Ghost'
ROOM_NUMBER = 0
FLOOR_NUMBER = 0
GUEST_LIST = []
ACCESS_KEY = ''
OPERATOR = 'check-in'   # (check-in | join | check-out)

# Guest Specific
GUEST_OF = 'Ghost'

# COLD PARAMETERS

FLOOR_ACCESS_KEYS = {}
HOTEL = None
FIFO_READER = None
FIFO_WRITTER = None
FILE_WRITTER = None
PREVIOUS_INSTRUCTION_SET = []
PREVIOUS_INSTRUCTION_RESPONSE = []

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

def fetch_file_writter_creation_values():
    log.debug('')
    creation_values = {
        'file_path': RESPONSE_FIFO,
        'log_name': SCRIPT_NAME,
    }
    return creation_values

def fetch_plaza_hotel_client_creation_values():
    log.debug('')
    creation_values = {
        'alias': ALIAS,
        'host': ADDRESS,
        'port': PORT_NUMBER,
        'room_buffer': BUFFER_SIZE,
        'client_name': SCRIPT_NAME,
        'room': ROOM_NUMBER,
        'floor': FLOOR_NUMBER,
        'timestamp_format': TIMESTAMP_FORMAT,
        'log_name': SCRIPT_NAME,
        'silent': SILENT,
    }
    return creation_values

def fetch_fifo_writter_creation_values():
    log.debug('')
    creation_values = {
        'fifo': RESPONSE_FIFO,
        'log_name': SCRIPT_NAME,
        'silent': SILENT,
    }
    return creation_values

def fetch_fifo_reader_creation_values():
    log.debug('')
    creation_values = {
        'fifo': STATE_FIFO,
        'log_name': SCRIPT_NAME,
        'silent': SILENT,
    }
    return creation_values

def fetch_plaza_hotel_creation_values():
    log.debug('')
    creation_values = {
        'state_file': STATE_FILE,
        'state_fifo': STATE_FIFO,
        'response_fifo': RESPONSE_FIFO,
        'floor_count': FLOOR_COUNT,
        'room_count': ROOM_COUNT,
        'room_capacity': CAPACITY,
        'log_name': SCRIPT_NAME,
        'silent': SILENT,
        'address': ADDRESS,
        'port_number': PORT_NUMBER,
        'key_file': KEY_FILE,
        'file_permissions': FILE_PERMISSIONS,
    }
    return creation_values

# UPDATERS

def update_floor_access_keys(key_map):
    global FLOOR_ACCESS_KEYS
    log.debug('')
    if not isinstance(key_map, dict):
        return error_invalid_floor_access_key_map(key_map)
    FLOOR_ACCESS_KEYS = key_map
    return FLOOR_ACCESS_KEYS

# CHECKERS

def check_previous_instruction_response(response):
    log.debug('')
    return response == PREVIOUS_INSTRUCTION_RESPONSE

def check_previous_instruction_set(instruction_set):
    log.debug('')
    return instruction_set == PREVIOUS_INSTRUCTION_SET

# CREATORS

def create_file_writter():
    log.debug('')
    creation_values = fetch_file_writter_creation_values()
    file_writter = PHFileWritter(**creation_values)
    return file_writter

def create_command_line_parser():
    log.debug('')
    parser = optparse.OptionParser(
        'Start PlazaHotel server -\n%prog \ \n'
        '   -n | --script-name=PlazaHotel \ \n'
        '   -m | --running-mode=server \ \n'
        '   -s | --silent-flag=off \ \n'
        '   -t | --timestamp-format=template-string \ \n'
        '   -f | --state-file=/state/file/path \ \n'
        '   -F | --state-fifo=/state/fifo/path \ \n'
        '   -R | --response-fifo=/response/fifo/path \ \n'
        '   -b | --buffer-size=4096 \ \n'
        '   -p | --port-number=8080 \ \n'
        '   -a | --address=127.0.0.1 \ \n'
        '   -H | --hotel-height=15 \ \n'
        '   -W | --hotel-width=5 \ \n'
        '   -C | --room-capacity=20 \ \n'
        '   -l | --log-file=/log/file/path \n\n'
        '   -P | --file-permissions=750 \n\n'
        '   -S | --static-floor-keys=/static/key/file'
        'Usage: Book room as client -\n%prog \ \n'
        '   -n | --script-name=PlazaHotel \ \n'
        '   -m | --running-mode=client \ \n'
        '   -s | --silent-flag=off \ \n'
        '   -t | --timestamp-format=template-string \ \n'
        '   -f | --state-file=/state/file/path \ \n'
        '   -F | --state-fifo=/state/fifo/path \ \n'
        '   -R | --response-fifo=/response/fifo/path \ \n'
        '   -b | --buffer-size=4096 \ \n'
        '   -p | --port-number=8080 \ \n'
        '   -a | --address=127.0.0.1 \ \n'
        '   -T | --client-type=client \ \n'
        '   -x | --floor-number=3 \ \n'
        '   -y | --room-number=13 \ \n'
        '   -N | --alias-name=DefaultClient \ \n'
        '   -A | --access-key=accessKey123 \ \n'
        '   -g | --guest-list=Guest1,Guest2,Guest3 \ \n'
        '   -o | --operation=check-in \ \n'
        '   -l | --log-file=/log/file/path \n\n'
        'Usage: Join room as guest -\n%prog \ \n'
        '   -n | --script-name=PlazaHotel \ \n'
        '   -m | --running-mode=client \ \n'
        '   -s | --silent-flag=off \ \n'
        '   -t | --timestamp-format=template-string \ \n'
        '   -f | --state-file=/state/file/path \ \n'
        '   -F | --state-fifo=/state/fifo/path \ \n'
        '   -R | --response-fifo=/response/fifo/path \ \n'
        '   -b | --buffer-size=4096 \ \n'
        '   -p | --port-number=8080 \ \n'
        '   -a | --address=127.0.0.1 \ \n'
        '   -T | --client-type=guest \ \n'
        '   -N | --alias-name=Guest1 \ \n'
        '   -c | --client-alias=DefaultClient \ \n'
        '   -o | --operation=join \ \n'
        '   -x | --floor-number=3 \ \n'
        '   -y | --room-number=13 \ \n'
        '   -l | --log-file=/log/file/path \n\n'
    )
    return parser

def create_plaza_hotel_chat_client():
    log.debug('')
    creation_values = fetch_plaza_hotel_client_creation_values()
    plaza_hotel_client = PHChatClient(**creation_values)
    return plaza_hotel_client

def create_fifo_writter():
    log.debug('')
    creation_values = fetch_fifo_writter_creation_values()
    fifo_writter = PHFifoWritter(**creation_values)
    return fifo_writter

def create_fifo_reader():
    log.debug('')
    creation_values = fetch_fifo_reader_creation_values()
    fifo_reader = PHFifoWritter(**creation_values)
    return fifo_reader

def create_plaza_hotel():
    log.debug('')
    creation_values = fetch_plaza_hotel_creation_values()
    hotel = PHHotel(**creation_values)
    return hotel

# GENERAL

def refresh_hotel_map(hotel):
    log.debug('')
    clear_screen()
    return hotel.display_hotel_map()

def clear_screen():
    log.debug('')
    return os.system('cls' if os.name == 'nt' else 'clear')

def stdout_msg(message):
    log.debug('')
    log.info(message)
    if SILENT == 'off':
        print(message)
        return True
    return False

# HANDLERS

#@pysnooper.snoop('../logs/plaza-hotel.log')
def handle_plaza_hotel_client_checkout(fifo_writter, fifo_reader):
    global OPERATOR
    global PREVIOUS_INSTRUCTION_RESPONSE
    log.debug('')
    OPERATOR = 'check-out'
    checkout_string = ALIAS + ',' + OPERATOR + ',' + str(ROOM_NUMBER) + ',' \
        + str(FLOOR_NUMBER)
    fifo_reader.write(content=checkout_string)
    response_count, response_body = 0, ''
    for response in fifo_writter.read():
        if response_count > 5:
            return error_server_response_timeout(response_body, response_count)
        instruction_response = ' '.join(
            [item.strip('\n').strip(' ') for item in response.split(' ')]
        )
        if check_previous_instruction_response(instruction_response):
            warning_duplicated_instruction_response(instruction_response)
            continue
        dst_alias = response.split(' ')[0].strip('\n').strip(' ')
        if not response or dst_alias != ALIAS:
            response_count += 1
            continue
        response_body = ' '.join(
            [item.strip('\n').strip(' ') for item in response.split(' ')[1:]]
        )
        PREVIOUS_INSTRUCTION_RESPONSE = instruction_response
        break
    if response_body != 'checked-out':
        display_plaza_hotel_separator('Connection broke abruptly!')
    return True if response_body == 'checked-out' else False

#@pysnooper.snoop('../logs/plaza-hotel.log')
def handle_plaza_hotel_guest_join(fifo_writter, fifo_reader):
    global OPERATOR
    global PREVIOUS_INSTRUCTION_RESPONSE
    log.debug('')
    OPERATOR = 'join'
    join_string = '{},{},{},{}'.format(ALIAS,GUEST_OF,OPERATOR,ACCESS_KEY)
    fifo_reader.write(content=join_string)
    response_count, response_body = 0, ''
    for response in fifo_writter.read():
        if response_count > 5:
            return error_server_response_timeout(join_string, response_count)
        instruction_response = ' '.join(
            [item.strip('\n').strip(' ') for item in response.split(' ')]
        )
        if check_previous_instruction_response(instruction_response):
            warning_duplicated_instruction_response(instruction_response)
            continue
        dst_alias = response.split(' ')[0].strip('\n').strip(' ')
        if not response or dst_alias != ALIAS:
            response_count += 1
            continue
        response_body = ' '.join(
            [item.strip('\n').strip(' ') for item in response.split(' ')[1:]]
        )
        PREVIOUS_INSTRUCTION_RESPONSE = instruction_response
        break
    return process_server_instruction_response(
        response_body, fifo_writter, fifo_reader
    )

#@pysnooper.snoop('../logs/plaza-hotel.log')
def handle_plaza_hotel_client_checkin(fifo_writter, fifo_reader):
    global OPERATOR
    global PREVIOUS_INSTRUCTION_RESPONSE
    log.debug('')
    OPERATOR = 'check-in'
    guest_string = ','.join(GUEST_LIST)
    checkin_string = '{},{},{},{},{},{}'.format(
            ALIAS,FLOOR_NUMBER,ACCESS_KEY,OPERATOR,ROOM_NUMBER,guest_string
        )
    fifo_reader.write(content=checkin_string)
    response_count, response_body = 0, ''
    for response in fifo_writter.read():
        if response_count > 5:
            return error_server_response_timeout(checkin_string, response_count)
        dst_alias = response.split(' ')[0].strip('\n').strip(' ')
        if not response or dst_alias != ALIAS:
            response_count += 1
            continue
        response_body = ' '.join(
            [item.strip('\n').strip(' ') for item in response.split(' ')[1:]]
        )
        break
    return process_server_instruction_response(
        response_body, fifo_writter, fifo_reader
    )

# DISPLAY

def display_plaza_hotel_separator(message=None):
    log.debug('')
    suffix = '' if not message else '{} ---'.format(message)
    separator = '\n---[ Plaza Hotel ]--- Whisper Rendezvous --- {}'.format(
        suffix
    )
    return stdout_msg(separator)

def display_plaza_hotel_banner():
    log.debug('')
    banner = '\n________________________________________________________________________________\n\n'\
        '  *                    *   Plaza Hotel - (v.Whispers)   *                    *  \n'\
        '________________________________________________________________________________\n'\
        '                     Regards, the Alveare Solutions society.\n'
    return stdout_msg(banner)

# PROCESSORS

def process_static_floor_keys_argument(parser, options):
    global STATIC_KEY_FILE
    log.debug('')
    file_path = options.static_keys
    if not file_path:
        log.warning(
            'No static floor access key file provided. '
            'Defaulting to ({}).'.format(STATIC_KEY_FILE)
        )
        return False
    STATIC_KEY_FILE = file_path
    stdout_msg(
        '[ + ]: Static floor keys setup ({}).'.format(STATIC_KEY_FILE)
    )
    return True

def process_file_permissions_argument(parser, options):
    global FILE_PERMISSIONS
    log.debug('')
    numeric_uog_permissions = options.file_permissions
    if not numeric_uog_permissions:
        log.warning(
            'No UOG file permissions provided. '
            'Defaulting to ({}).'.format(FILE_PERMISSIONS)
        )
        return False
    FILE_PERMISSIONS = numeric_uog_permissions
    stdout_msg(
        '[ + ]: File permissions setup ({}).'.format(FILE_PERMISSIONS)
    )
    return True

def process_log_file_argument(parser, options):
    global log
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
    log = log_init(SCRIPT_NAME)
    stdout_msg(
        '[ + ]: Log file setup ({}).'.format(os.path.basename(LOG_FILE_PATH))
    )
    return True

def process_key_file_argument(parser, options):
    global KEY_FILE
    log.debug('')
    file_path = options.key_file
    if not file_path:
        log.warning(
            'No key file path provided. '
            'Defaulting to ({}).'.format(KEY_FILE)
        )
        return False
    KEY_FILE = file_path
    stdout_msg(
        '[ + ]: Key file setup ({}).'.format(KEY_FILE)
    )
    return True

def process_client_instructions_update_load(hotel, instruction_set):
    log.debug('')
    if instruction_set[1] == '.update':
        return hotel.update_hotel_map()
    elif instruction_set[1] == '.load':
        return hotel.load_hotel_map()
    return False

def process_client_instructions_checkout_join(hotel, instruction_set, fifo_writter):
    log.debug('')
    alias = instruction_set[0]
    if len(instruction_set) < 3:
        warning_invalid_instruction_set(instruction_set)
        return fifo_writter.write(content=alias + ' invalid-instruction')
    if instruction_set[2] == 'join':
        join = hotel.join_room(
            guest=alias, client=instruction_set[1],
            instruction_set=instruction_set
        )
        response = 'access-granted' if join else 'access-denied'
        refresh_hotel_map(hotel)
        return fifo_writter.write(content=alias + ' ' + response)
    elif instruction_set[1] == 'check-out':
        checkout = hotel.checkout_room(
            client=instruction_set[0],
            room_number=int(instruction_set[2]),
            floor_number=int(instruction_set[3])
        )
        message = 'checked-out' if checkout else 'not-checked-out'
        refresh_hotel_map(hotel)
        return fifo_writter.write(content=alias + ' ' + message)
    return False

def process_client_instruction_checkin(hotel, instruction_set, fifo_writter):
    log.debug('')
    try:
        alias = instruction_set[0]
        floor = int(instruction_set[1])
        access_key = instruction_set[2]
        operator = instruction_set[3]
        room = int(instruction_set[4])
        guest_list = [
            guest.strip('\n').strip(' ') for guest in instruction_set[5:] if guest
        ]
    except Exception as e:
        warning_invalid_instruction_set(instruction_set, e)
        return fifo_writter.write(content='{} access-denied'.format(alias))
    if access_key and access_key not in FLOOR_ACCESS_KEYS.values():
        warning_invalid_floor_access_key(floor, instruction_set)
        return fifo_writter.write(content='{} access-denied'.format(alias))
    elif floor in FLOOR_ACCESS_KEYS and FLOOR_ACCESS_KEYS[floor] != access_key:
        warning_access_key_denied(access_key, instruction_set)
        return fifo_writter.write(content='{} access-denied'.format(alias))
    if operator == 'check-in':
        checkin = hotel.checkin_room(
            client=alias, floor_number=floor, room_number=room,
            access_key=access_key, guest_list=guest_list
        )
        refresh_hotel_map(hotel)
        if not checkin:
            warning_could_not_client_checkin_failure(
                alias, floor,access_key, operator, room, guest_list
            )
            return fifo_writter.write(content='{} access-denied'.format(alias))
    else:
        warning_invalid_operator(operator, instruction_set)
        return fifo_writter.write(
            content='{} invalid-operator,{}'.format(alias, operator)
        )
    return False

#@pysnooper.snoop(LOG_FILE_PATH)
def process_client_instruction(instruction, hotel, fifo_reader, fifo_writter):
    global PREVIOUS_INSTRUCTION_SET
    log.debug('')
    if instruction in ('', ' ', '\n'):
        return
    instruction_set = instruction.split(',')
    if len(instruction_set) < 2:
        warning_invalid_instruction_set(instruction_set)
        return fifo_writter.write('invalid-instruction')
    elif check_previous_instruction_set(instruction_set):
        return
    PREVIOUS_INSTRUCTION_SET = instruction_set
    alias = instruction_set[0]
    processed = process_client_instructions_update_load(hotel, instruction_set)
    if processed:
        return processed
    processed = process_client_instructions_checkout_join(
        hotel, instruction_set, fifo_writter
    )
    if processed:
        return processed
    processed = process_client_instruction_checkin(
        hotel, instruction_set, fifo_writter
    )
    if processed:
        return processed
    time.sleep(1)
    return fifo_writter.write(content='{} access-granted'.format(alias))

def process_operation_argument(parser, options):
    global OPERATOR
    log.debug('')
    action = options.operation
    if not action:
        log.warning(
            'No operation instruction provided. '
            'Defaulting to ({}).'.format(OPERATOR)
        )
        return False
    OPERATOR = action
    stdout_msg(
        '[ + ]: Action setup ({}).'.format(OPERATOR)
    )
    return True

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

def process_script_name_argument(parser, options):
    global SCRIPT_NAME
    log.debug('')
    script_name = options.script_name
    if not script_name:
        log.warning(
            'No script name provided. '
            'Defaulting to ({}).'.format(SCRIPT_NAME)
        )
        return False
    SCRIPT_NAME = script_name
    stdout_msg(
        '[ + ]: Script name setup ({}).'.format(SCRIPT_NAME)
    )
    return True

def process_running_mode_argument(parser, options):
    global RUNNING_MODE
    log.debug('')
    running_mode = options.running_mode
    if not running_mode:
        log.warning(
            'No running mode provided. '
            'Defaulting to ({}).'.format(RUNNING_MODE)
        )
        return False
    RUNNING_MODE = running_mode
    stdout_msg(
        '[ + ]: Running mode setup ({}).'.format(RUNNING_MODE)
    )
    return True

def process_timestamp_format_argument(parser, options):
    global TIMESTAMP_FORMAT
    log.debug('')
    tformat = options.timestamp_format
    if not tformat:
        log.warning(
            'No timestamp format template string provided. '
            'Defaulting to ({}).'.format(TIMESTAMP_FORMAT)
        )
        return False
    TIMESTAMP_FORMAT = tformat
    stdout_msg(
        '[ + ]: Timestamp format setup ({}).'.format(TIMESTAMP_FORMAT)
    )
    return True

def process_state_file_argument(parser, options):
    global STATE_FILE
    log.debug('')
    state_file = options.state_file
    if not state_file:
        log.warning(
            'No server state file path provided. '
            'Defaulting to ({}).'.format(STATE_FILE)
        )
        return False
    STATE_FILE = state_file
    stdout_msg(
        '[ + ]: Server state file path setup ({}).'.format(STATE_FILE)
    )
    return True

def process_state_fifo_argument(parser, options):
    global STATE_FIFO
    log.debug('')
    state_fifo = options.state_fifo
    if not state_fifo:
        log.warning(
            'No server state fifo path provided. '
            'Defaulting to ({}).'.format(STATE_FIFO)
        )
        return False
    STATE_FIFO = state_fifo
    stdout_msg(
        '[ + ]: Server state fifo path setup ({}).'.format(STATE_FIFO)
    )
    return True

def process_response_fifo_argument(parser, options):
    global RESPONSE_FIFO
    log.debug('')
    response_fifo = options.response_fifo
    if not response_fifo:
        log.warning(
            'No server response fifo path provided. '
            'Defaulting to ({}).'.format(RESPONSE_FIFO)
        )
        return False
    RESPONSE_FIFO = response_fifo
    stdout_msg(
        '[ + ]: Server response fifo path setup ({}).'.format(RESPONSE_FIFO)
    )
    return True

def process_buffer_size_argument(parser, options):
    global BUFFER_SIZE
    log.debug('')
    buffer_size = options.buffer_size
    if not buffer_size:
        log.warning(
            'No buffer size provided. '
            'Defaulting to ({}).'.format(BUFFER_SIZE)
        )
        return False
    BUFFER_SIZE = buffer_size
    stdout_msg(
        '[ + ]: Chatroom buffer size (bytes) setup ({}).'.format(BUFFER_SIZE)
    )
    return True

def process_hotel_height_argument(parser, options):
    global FLOOR_COUNT
    log.debug('')
    floor_count = options.hotel_height
    if not floor_count:
        log.warning(
            'No hotel height provided. '
            'Defaulting to ({}).'.format(FLOOR_COUNT)
        )
        return False
    FLOOR_COUNT = floor_count
    stdout_msg(
        '[ + ]: Hotel height setup ({}).'.format(FLOOR_COUNT)
    )
    return True

def process_hotel_width_argument(parser, options):
    global ROOM_COUNT
    log.debug('')
    room_count = options.hotel_width
    if not room_count:
        log.warning(
            'No hotel width provided. '
            'Defaulting to ({}).'.format(ROOM_COUNT)
        )
        return False
    ROOM_COUNT = room_count
    stdout_msg(
        '[ + ]: Hotel width setup ({}).'.format(ROOM_COUNT)
    )
    return True

def process_room_capacity_argument(parser, options):
    global CAPACITY
    log.debug('')
    room_capacity = options.capacity
    if not room_capacity:
        log.warning(
            'No room capacity provided. '
            'Defaulting to ({}).'.format(CAPACITY)
        )
        return False
    CAPACITY = room_capacity
    stdout_msg(
        '[ + ]: Room capacity setup ({}).'.format(CAPACITY)
    )
    return True

def process_client_type_argument(parser, options):
    global CLIENT_TYPE
    log.debug('')
    client_type = options.client_type
    if not client_type:
        log.warning(
            'No client category type provided. '
            'Defaulting to ({}).'.format(CLIENT_TYPE)
        )
        return False
    CLIENT_TYPE = client_type
    stdout_msg(
        '[ + ]: Client type setup ({}).'.format(CLIENT_TYPE)
    )
    return True

def process_port_number_argument(parser, options):
    global PORT_NUMBER
    log.debug('')
    port_number = options.port_number
    if not port_number:
        log.warning(
            'No port number provided. '
            'Defaulting to ({}).'.format(PORT_NUMBER)
        )
        return False
    PORT_NUMBER = port_number
    stdout_msg(
        '[ + ]: Target port number setup ({}).'.format(PORT_NUMBER)
    )
    return True

def process_coordinate_floor_argument(parser, options):
    global FLOOR_NUMBER
    log.debug('')
    floor_number = options.coordinate_floor
    if not floor_number:
        log.warning(
            'No floor number coordinate provided. '
            'Defaulting to ({}).'.format(FLOOR_NUMBER)
        )
        return False
    FLOOR_NUMBER = floor_number
    stdout_msg(
        '[ + ]: Target floor number setup ({}).'.format(FLOOR_NUMBER)
    )
    return True

def process_coordinate_room_argument(parser, options):
    global ROOM_NUMBER
    log.debug('')
    room_number = options.coordinate_room
    if not room_number:
        log.warning(
            'No room number coordinate provided. '
            'Defaulting to ({}).'.format(ROOM_NUMBER)
        )
        return False
    ROOM_NUMBER = room_number
    stdout_msg(
        '[ + ]: Target room number setup ({}).'.format(ROOM_NUMBER)
    )
    return True

def process_address_argument(parser, options):
    global ADDRESS
    log.debug('')
    address = options.address
    if not address:
        log.warning(
            'No nickname (alias) provided. '
            'Defaulting to ({}).'.format(ADDRESS)
        )
        return False
    ADDRESS = address
    stdout_msg(
        '[ + ]: Target server address setup ({}).'.format(ADDRESS)
    )
    return True

def process_alias_argument(parser, options):
    global ALIAS
    log.debug('')
    alias = options.alias_nickname
    if not alias:
        log.warning(
            'No nickname (alias) provided. '
            'Defaulting to ({}).'.format(ALIAS)
        )
        return False
    ALIAS = alias
    stdout_msg(
        '[ + ]: Nickname (alias) setup ({}).'.format(ALIAS)
    )
    return True

def process_access_key_argument(parser, options):
    global ACCESS_KEY
    log.debug('')
    access_key = options.access_key
    if not access_key:
        log.warning(
            'No floor access key provided. '
            'Defaulting to ({}).'.format(ACCESS_KEY)
        )
        return False
    ACCESS_KEY = access_key
    stdout_msg(
        '[ + ]: Floor access key setup ({}).'.format(ACCESS_KEY)
    )
    return True

def process_expected_guests_argument(parser, options):
    global GUEST_LIST
    log.debug('')
    guest_string = options.expected_guests
    guest_list = [] if not guest_string else guest_string.split(',')
    if not guest_list:
        log.warning(
            'No expected guest aliases provided. '
            'Defaulting to ({}).'.format(GUEST_LIST)
        )
        return False
    GUEST_LIST = guest_list
    stdout_msg(
        '[ + ]: Expected guest aliases setup ({}).'.format(GUEST_LIST)
    )
    return True

def process_expecting_client_argument(parser, options):
    global GUEST_OF
    log.debug('')
    client_alias = options.expecting_client
    if client_alias == None:
        log.warning(
            'No expecting client alias provided. '
            'Defaulting to ({}).'.format(GUEST_OF)
        )
        return False
    GUEST_OF = client_alias
    stdout_msg(
        '[ + ]: Expecting client alias setup ({}).'.format(GUEST_OF)
    )
    return True

def process_command_line_options(parser):
    log.debug('')
    (options, args) = parser.parse_args()
    # [ NOTE ]: If you trully want to be covert, process silent_flag first
    stdout_msg('[...]: Processing CLI options:')
    processed = {
        'silent_flag': process_silent_flag_argument(parser, options),
        'log_file': process_log_file_argument(parser, options),
        'script_name': process_script_name_argument(parser, options),
        'running_mode': process_running_mode_argument(parser, options),
        'timestamp_format': process_timestamp_format_argument(parser, options),
        'state_file': process_state_file_argument(parser, options),
        'state_fifo': process_state_fifo_argument(parser, options),
        'response_fifo': process_response_fifo_argument(parser, options),
        'buffer_size': process_buffer_size_argument(parser, options),
        'hotel_height': process_hotel_height_argument(parser, options),
        'hotel_width': process_hotel_width_argument(parser, options),
        'capacity': process_room_capacity_argument(parser, options),
        'client_type': process_client_type_argument(parser, options),
        'port_number': process_port_number_argument(parser, options),
        'coordinate_floor': process_coordinate_floor_argument(parser, options),
        'coordinate_room': process_coordinate_room_argument(parser, options),
        'address': process_address_argument(parser, options),
        'alias_nickname': process_alias_argument(parser, options),
        'access_key': process_access_key_argument(parser, options),
        'expected_guests': process_expected_guests_argument(parser, options),
        'expecting_client': process_expecting_client_argument(parser, options),
        'operation': process_operation_argument(parser, options),
        'key_file': process_key_file_argument(parser, options),
        'file_permissions': process_file_permissions_argument(parser, options),
        'static_floor_keys': process_static_floor_keys_argument(parser, options),
    }
    return processed

def process_server_access_granted_response(segmented_response,
                                           fifo_writter, fifo_reader):
    log.debug('')
    display_plaza_hotel_separator('Access Granted!')
    im_client = create_plaza_hotel_chat_client()
    try:
        im_client.client_init()
    finally:
        try:
            handle_plaza_hotel_client_checkout(fifo_writter, fifo_reader)
        except Exception as e:
            log.error(e)
    return True

#@pysnooper.snoop('../logs/plaza-hotel.log')
def process_server_instruction_response(response_body, fifo_writter, fifo_reader):
    log.debug('')
    segmented_body = response_body.split(',')
    handlers = {
        'access-granted': process_server_access_granted_response,
        'access-denied': process_server_access_denied_response,
        'invalid_operator': process_server_invalid_operator_response,
        'checked-out': process_server_client_checked_out_response,
    }
    if segmented_body[0] not in handlers:
        return error_malformed_server_response(
            segmented_body[0], segmented_body
        )
    return handlers[segmented_body[0]](segmented_body, fifo_writter, fifo_reader)

def process_server_client_checked_out_response(segmented_response,
                                          fifo_writter, fifo_reader):
    log.debug('')
    return display_plaza_hotel_separator('Checked Out!')

def process_server_access_denied_response(segmented_response,
                                          fifo_writter, fifo_reader):
    log.debug('')
    return display_plaza_hotel_separator('Access Denied!')

def process_server_invalid_operator_response(segmented_response,
                                             fifo_writter, fifo_reader):
    log.debug('')
    return display_plaza_hotel_separator('Invalid Operator!')

# INIT

#@pysnooper.snoop()
def init_plaza_hotel_server():
    global FLOOR_ACCESS_KEYS
    global HOTEL
    global FIFO_READER
    global FIFO_WRITTER
    global STATIC_KEY_FILE
    log.debug('')
    HOTEL = create_plaza_hotel()
    access_keys = {}
    if STATIC_KEY_FILE and os.path.exists(STATIC_KEY_FILE):
        FILE_WRITTER = create_file_writter()
        content = FILE_WRITTER.read(target_file=STATIC_KEY_FILE)
        access_keys = {}
        if content:
            for fl_line in content:
                if fl_line[0] == "#":
                    continue
                split_line = fl_line.split(' ')
                if len(split_line) != 2:
                    continue
                hotel_floor, floor_key = split_line[0], split_line[1]
                access_keys.update({hotel_floor: floor_key.strip('\n')})
    HOTEL.setup(**access_keys)
    update_floor_access_keys(HOTEL.fetch_floor_access_keys())
    FIFO_READER, FIFO_WRITTER = create_fifo_reader(), create_fifo_writter()
    FIFO_READER.setup()
    FIFO_WRITTER.setup()
    try:
        HOTEL.display_hotel_map()
        for instruction in FIFO_READER.read():
            if not instruction:
                continue
            thread = threading.Thread(
                target=process_client_instruction,
                args=(instruction, HOTEL, FIFO_READER, FIFO_WRITTER)
            )
            thread.daemon = True
            thread.start()
            time.sleep(0.2)
            refresh_hotel_map(HOTEL)
    finally:
        HOTEL.cleanup()
        FIFO_READER.cleanup()
        FIFO_WRITTER.cleanup()

def init_plaza_hotel():
    parse_command_line_arguments()
    plaza_hotel = {
        'client': init_plaza_hotel_client,
        'server': init_plaza_hotel_server,
    }
    if RUNNING_MODE not in plaza_hotel:
        return error_invalid_running_mode(
            RUNNING_MODE, list(plaza_hotel.keys())
        )
    return plaza_hotel[RUNNING_MODE]()

#@pysnooper.snoop()
def init_plaza_hotel_client():
    global FIFO_READER
    global FIFO_WRITTER
    log.debug('')
    FIFO_READER, FIFO_WRITTER = create_fifo_reader(), create_fifo_writter()
    FIFO_READER.setup()
    FIFO_WRITTER.setup()
    handlers = {
        'client': handle_plaza_hotel_client_checkin,
        'guest': handle_plaza_hotel_guest_join,
    }
    if CLIENT_TYPE not in handlers:
        return error_invalid_client_type(CLIENT_TYPE, list(handlers.keys()))
    return handlers[CLIENT_TYPE](FIFO_WRITTER, FIFO_READER)

# PARSERS

def add_command_line_parser_general_options(parser):
    log.debug('')
    parser.add_option(
        '-n', '--script-name', dest='script_name', type='string',
        help='Program Label - Eases the rebranding of the Plaza Hotel '
        'project,', metavar='NAME'
    )
    parser.add_option(
        '-m', '--running-mode', dest='running_mode', type='string',
        help='Running Mode - Manages server, clients and guests.',
        metavar='(server | client)'
    )
    parser.add_option(
        '-s', '--silent-flag', dest='silent_flag', type='string',
        help='Silence STDOUT Output.', metavar='(on | off)'
    )
    parser.add_option(
        '-t', '--timestamp-format', dest='timestamp_format', type='string',
        help='Timestamp Format Template.', metavar='TEMPLATE'
    )
    parser.add_option(
        '-f', '--state-file', dest='state_file', type='string',
        help='Server State File Path.', metavar='FILE_PATH'
    )
    parser.add_option(
        '-F', '--state-fifo', dest='state_fifo', type='string',
        help='Server State Fifo Path.', metavar='FIFO_PATH'
    )
    parser.add_option(
        '-R', '--response-fifo', dest='response_fifo', type='string',
        help='Server Response Fifo Path.', metavar='FIFO_PATH'
    )
    parser.add_option(
        '-b', '--buffer-size', dest='buffer_size', type='int',
        help='Chatroom Bufer Size in Bytes.', metavar='BYTES'
    )
    parser.add_option(
        '-p', '--port-number', dest='port_number', type='int',
        help='Port Number - Socket binding port.', metavar='PORT'
    )
    parser.add_option(
        '-P', '--file-permissions', dest='file_permissions', type='int',
        help='File Permissions - Numeric UNIX permissions for state file '
        'and message pipes.', metavar='UOG'
    )
    parser.add_option(
        '-a', '--address', dest='address', type='string',
        help='Server Address - Socket binding address.',
        metavar='IPv4'
    )
    parser.add_option(
        '-K', '--key-file', dest='key_file', type='string',
        help='Key File Path - Where floor access keys are stored on disk.',
        metavar='FILE_PATH'
    )
    parser.add_option(
        '-l', '--log-file', dest='log_file', type='string',
        help='Log File Path - File to log messages to.',
        metavar='FILE_PATH'
    )
    return parser

def add_command_line_parser_server_options(parser):
    log.debug('')
    parser.add_option(
        '-H', '--hotel-height', dest='hotel_height', type='int',
        help='Hotel Height - Number of floors. Implies (-m server)',
        metavar='FLOOR_COUNT'
    )
    parser.add_option(
        '-W', '--hotel-width', dest='hotel_width', type='int',
        help='Hotel Width - Number of rooms on each floor. Implies (-m server)',
        metavar='ROOM_COUNT'
    )
    parser.add_option(
        '-C', '--room-capacity', dest='capacity', type='int',
        help='Room Capacity - Number of orbitals allowed in each room. '
        'Implies (-m server)', metavar='ORBITAL_COUNT'
    )
    parser.add_option(
        '-S', '--static-floor-keys', dest='static_keys', type='string',
        help='Static Floor Access Keys. '
        'Implies (-m server)', metavar='FILE_PATH'
    )
    return parser

def add_command_line_parser_client_options(parser):
    log.debug('')
    parser.add_option(
        '-T', '--client-type', dest='client_type', type='string',
        help='Chatroom Client Type - Client user category type. '
        'Implies (-m client)', metavar='(client | guest)'
    )
    parser.add_option(
        '-x', '--floor-number', dest='coordinate_floor', type='int',
        help='Target Floor Number - Floor you want to access chatroom on. '
        'Implies (-m client -T client)', metavar='FLOOR'
    )
    parser.add_option(
        '-y', '--room-number', dest='coordinate_room', type='int',
        help='Target Room Number - Room you want to enter. '
        'Implies (-m client -T client)', metavar='ROOM'
    )
    parser.add_option(
        '-N', '--alias', dest='alias_nickname', type='string',
        help='Nickname - The alias other orbitals will identify you after. '
        'Implies (-m client)', metavar='NICKNAME'
    )
    parser.add_option(
        '-A', '--access-key', dest='access_key', type='string',
        help='Floor Access Key - Character sequence that grants you access '
        'to the chatrooms on a given floor. Implies (-m client -T client)',
        metavar='KEY'
    )
    parser.add_option(
        '-g', '--guest-list', dest='expected_guests', type='string',
        help='Expected Guests - (Optional) Comma separated list of user '
        'aliases you are expecting to join the chatroom. If no guest list'
        'is specified, anybody can join the booked chatroom.'
        'Implies (-m client -T client)',
        metavar='GUEST1,GUEST2'
    )
    parser.add_option(
        '-c', '--client-alias', dest='expecting_client', type='string',
        help='Expecting Client - Alias of the user that booked a room '
        'and has you on his guest list. Implies (-m client -T guest)',
        metavar='ALIAS'
    )
    parser.add_option(
        '-o', '--operation', dest='operation', type='string',
        help='Client action - First issued instruction to server.',
        metavar='ACTION'
    )
    return parser

def add_command_line_parser_options(parser):
    log.debug('')
    add_command_line_parser_general_options(parser)
    add_command_line_parser_server_options(parser)
    add_command_line_parser_client_options(parser)
    return parser

#@pysnooper.snoop()
def parse_command_line_arguments():
    log.debug('')
    parser = create_command_line_parser()
    add_parser_options = add_command_line_parser_options(parser)
    return process_command_line_options(parser)

# WARNINGS

def warning_duplicated_instruction_response(*args):
    log.warning(
        'Duplicated server instruction response. '
        'Details: {}'.format(args)
    )
    return False

def warning_could_not_client_checkin_failure(*args):
    log.warning('Client checkin failure. Details: {}'.format(args))
    return False

def warning_unknown_user_alias(*args):
    log.warning('Unknown user alias. Details: {}'.format(args))
    return False

def warning_invalid_operator(*args):
    log.warning('Invalid operator. Details: {}'.format(args))
    return False

def warning_invalid_instruction_set(*args):
    log.warning('Invalid instruction set. Details: {}'.format(args))
    return False

def warning_invalid_floor_access_key(*args):
    log.warning('Invalid floor access key. Details: {}'.format(args))
    return False

def warning_access_key_denied(*args):
    log.warning('Access key denied. Details: {}'.format(args))
    return False

# ERRORS

def error_invalid_client_type(*args):
    log.error('Invalid client type. Details: {}'.format(args))
    return False

def error_malformed_server_response(*args):
    log.error('Malformed server response. Details: {}'.format(args))
    return False

def error_server_response_timeout(*args):
    log.error('Server response timeout. Details: {}'.format(args))
    return False

def error_invalid_floor_access_key_map(*args):
    log.error('Invalid floor access keys map. Details: {}'.format(args))
    return False

def error_invalid_running_mode(*args):
    log.error('Invalid running mode. Details: {}'.format(args))
    return False

# MISCELLANEOUS

if __name__ == '__main__':
    clear_screen()
    display_plaza_hotel_banner()
    init_plaza_hotel()

# CODE DUMP
