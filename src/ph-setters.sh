#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# SETTERS

function set_server_state_guests () {
    local GUEST_LINES="$@"
    PH_SERVER_STATE['guests']="$GUEST_LINES"
    return 0
}

function set_server_state_clients () {
    local CLIENT_LINES="$@"
    PH_SERVER_STATE['clients']="$CLIENT_LINES"
    return 0
}

function set_server_state_rooms () {
    local ROOM_LINES="$@"
    PH_SERVER_STATE['rooms']="$ROOM_LINES"
    return 0
}

function set_server_state_floors () {
    local FLOOR_LINES="$@"
    PH_SERVER_STATE['floors']="$FLOOR_LINES"
    return 0
}

function set_hotel_height () {
    local FLOOR_COUNT=$1
    check_value_is_number $FLOOR_COUNT
    if [ $? -ne 0 ]; then
        error_msg "Floor count must be a number, not (${RED}$FLOOR_COUNT${RESET})."
        return 1
    fi
    MD_DEFAULT['floor-count']=$FLOOR_COUNT
    return 0
}

function set_hotel_width () {
    local ROOM_COUNT=$1
    check_value_is_number $ROOM_COUNT
    if [ $? -ne 0 ]; then
        error_msg "Room count must be a number, not (${RED}$ROOM_COUNT${RESET})."
        return 1
    fi
    MD_DEFAULT['room-count']=$ROOM_COUNT
    return 0
}

function set_room_capacity () {
    local CAPACITY=$1
    check_value_is_number $CAPACITY
    if [ $? -ne 0 ]; then
        error_msg "Room capacity must be a number, not (${RED}$CAPACITY${RESET})."
        return 1
    fi
    MD_DEFAULT['room-capacity']=$CAPACITY
    return 0
}

function set_room_buffer_size () {
    local BUFFER_SIZE=$1
    check_value_is_number $BUFFER_SIZE
    if [ $? -ne 0 ]; then
        error_msg "Room buffer size must be a number, not (${RED}$BUFFER_SIZE${RESET})."
        return 1
    fi
    MD_DEFAULT['buffer-size']=$BUFFER_SIZE
    return 0
}

function set_room_port_number () {
    local PORT_NUMBER=$1
    check_value_is_number $PORT_NUMBER
    if [ $? -ne 0 ]; then
        error_msg "Room port must be a number, not (${RED}$PORT_NUMBER${RESET})."
        return 1
    fi
    MD_DEFAULT['port-number']=$PORT_NUMBER
    return 0
}

function set_server_address () {
    local ADDRESS="$1"
    check_is_ipv4_address "$ADDRESS"
    if [ $? -ne 0 ]; then
        error_msg "Server address must be IPv4, not (${RED}$ADDRESS${RESET})."
        return 1
    fi
    MD_DEFAULT['address']="$ADDRESS"
    return 0
}

function set_alias () {
    local ALIAS="$1"
    MD_DEFAULT['alias']="$ALIAS"
    return 0
}

function set_guest_list () {
    local GUEST_LIST="$1"
    MD_DEFAULT['guest-list']="$GUEST_LIST"
    return 0
}

function set_guest_of_alias () {
    local GUEST_OF="$1"
    MD_DEFAULT['guest-of']="$GUEST_OF"
    return 0
}

function set_target_room_number () {
    local ROOM_NUMBER=$1
    check_value_is_number $ROOM_NUMBER
    if [ $? -ne 0 ]; then
        error_msg "Room number must be a number, not (${RED}$ROOM_NUMBER${RESET})."
        return 1
    fi
    MD_DEFAULT['room-number']=$ROOM_NUMBER
    return 0
}

function set_target_floor_number () {
    local FLOOR_NUMBER=$1
    check_value_is_number $FLOOR_NUMBER
    if [ $? -ne 0 ]; then
        error_msg "Floor number must be a number, not (${RED}$FLOOR_NUMBER${RESET})."
        return 1
    fi
    MD_DEFAULT['floor-level']=$FLOOR_NUMBER
    return 0
}

function set_floor_access_key () {
    local ACCESS_KEY="$1"
    MD_DEFAULT['access-key']="$ACCESS_KEY"
    return 0
}

function set_client_system_user_name () {
    local SYSTEM_USER="$1"
    MD_DEFAULT['system-user']="$SYSTEM_USER"
    return 0
}

function set_client_category_type () {
    local CLIENT_TYPE="$1"
    if [[ "$CLIENT_TYPE" != 'client' ]] && [[ "$CLIENT_TYPE" != 'guest' ]]; then
        error_msg "Unsupported client category type (${RED}$CLIENT_TYPE${RESET})"\
            "for version (${RED}$PH_VERSION${RESET})."
            "Defaulting to (${MAGENTA}${MD_DEFAULT['client-type']}${RESET})."
        return 1
    fi
    MD_DEFAULT['client-type']="$CLIENT_TYPE"
    return 0
}

function set_client_action () {
    local CLIENT_ACTION="$1"
    if [[ "$CLIENT_ACTION" != 'check-in' ]] && [[ "$CLIENT_ACTION" != 'join' ]]; then
        error_msg "Unsupported client action (${RED}$CLIENT_ACTION${RESET})"\
            "for version (${RED}$PH_VERSION${RESET})."
            "Defaulting to (${MAGENTA}${MD_DEFAULT['client-action']}${RESET})."
        return 1
    fi
    MD_DEFAULT['client-action']="$CLIENT_ACTION"
    return 0
}

function set_server_state_file () {
    local FILE_PATH="$1"
    MD_DEFAULT['state-file']="$FILE_PATH"
    return 0
}

function set_server_state_fifo () {
    local FIFO_PATH="$1"
    MD_DEFAULT['state-fifo']="$FIFO_PATH"
    return 0
}

function set_server_response_fifo () {
    local FIFO_PATH="$1"
    MD_DEFAULT['response-fifo']="$FIFO_PATH"
    return 0
}

function set_floor_access_key_file () {
    local KEY_FILE="$1"
    MD_DEFAULT['key-file']="$KEY_FILE"
    return 0
}
