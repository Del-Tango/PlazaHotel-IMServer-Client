#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# FETCHERS

function fetch_explore_room_number_from_user () {
    local FLOOR_LEVEL=$1
    while :
    do
        ROOM_NUMBER=`fetch_data_from_user 'RoomNumber'`
        if [ $? -ne 0 ]; then
            return 1
        fi
        check_value_is_number $ROOM_NUMBER
        if [ $? -ne 0 ]; then
            continue
        fi
        check_client_room_explore $ROOM_NUMBER $FLOOR_LEVEL
        if [ $? -ne 0 ]; then
            debug_msg "Client can not network on"\
                "floor (${RED}$FLOOR_LEVEL${RESET}),"\
                "room (${RED}$ROOM_NUMBER${RESET})."
            continue
        fi; break
    done
    echo $ROOM_NUMBER
    return $?
}

function fetch_floor_level_from_user () {
    while :
    do
        FLOOR_LEVEL=`fetch_data_from_user 'FloorLevel'`
        if [ $? -ne 0 ]; then
            return 1
        fi
        check_value_is_number $FLOOR_LEVEL
        if [ $? -ne 0 ]; then
            continue
        fi
        check_is_valid_floor_level $FLOOR_LEVEL
        if [ $? -ne 0 ]; then
            debug_msg "(${RED}$FLOOR_LEVEL${RESET}) is not a valid"\
                "(${BLUE}$SCRIPT_NAME${RESET}) floor level."
            continue
        fi; break
    done
    echo $FLOOR_LEVEL
    return $?
}

function fetch_floor_access_key_from_user () {
    FLOOR_ACCESS_KEY=`fetch_data_from_user 'AccessKey'`
    if [ $? -ne 0 ]; then
        return 1
    fi
    echo "$FLOOR_ACCESS_KEY"
    return $?
}

function fetch_checkin_room_number_from_user () {
    local FLOOR_LEVEL=$1
    while :
    do
        ROOM_NUMBER=`fetch_data_from_user 'RoomNumber'`
        if [ $? -ne 0 ]; then
            return 1
        fi
        check_value_is_number $ROOM_NUMBER
        if [ $? -ne 0 ]; then
            continue
        fi
        check_client_room_checkin $ROOM_NUMBER $FLOOR_LEVEL
        if [ $? -ne 0 ]; then
            debug_msg "Can not check in client on"\
                "floor (${RED}$FLOOR_LEVEL${RESET}),"\
                "room (${RED}$ROOM_NUMBER${RESET})."
            continue
        fi; break
    done
    echo $ROOM_NUMBER
    return $?
}

function fetch_server_state_cached_floor_lines () {
    FLOOR_LINES=()
    IFS='$'
    for cached_line in ${PH_SERVER_STATE['floors']}; do
        SANITIZED_LINE=`echo $cached_line | tr ' ' ',' | tr '\n' ' ' | sed -e 's/^ //g' -e 's/ $//g'`
        FLOOR_LINES=( ${FLOOR_LINES[@]} "$SANITIZED_LINE" )
    done
    IFS=' '
    echo ${FLOOR_LINES[@]}
    return $?
}

function fetch_server_state_cached_room_lines () {
    ROOM_LINES=()
    IFS='$'
    for cached_line in ${PH_SERVER_STATE['rooms']}; do
        SANITIZED_LINE=`echo $cached_line | tr ' ' ',' | tr '\n' ' ' | sed -e 's/^ //g' -e 's/ $//g'`
        ROOM_LINES=( ${ROOM_LINES[@]} "$SANITIZED_LINE" )
    done
    IFS=' '
    echo ${ROOM_LINES[@]}
    return $?
}

function fetch_server_state_cached_client_lines () {
    CLIENT_LINES=()
    IFS='$'
    for cached_line in ${PH_SERVER_STATE['clients']}; do
        SANITIZED_LINE=`echo $cached_line | tr ' ' ',' | tr '\n' ' ' | sed -e 's/^ //g' -e 's/ $//g'`
        CLIENT_LINES=( ${CLIENT_LINES[@]} "$SANITIZED_LINE" )
    done
    IFS=' '
    echo ${CLIENT_LINES[@]}
    return $?
}

function fetch_server_state_cached_guest_lines () {
    GUEST_LINES=()
    IFS='$'
    for cached_line in ${PH_SERVER_STATE['guests']}; do
        SANITIZED_LINE=`echo $cached_line | tr ' ' ',' | tr '\n' ' ' | sed -e 's/^ //g' -e 's/ $//g'`
        GUEST_LINES=( ${GUEST_LINES[@]} "$SANITIZED_LINE" )
    done
    IFS=' '
    echo ${GUEST_LINES[@]}
    return $?
}

function fetch_state_file_floor_start_pattern () {
    echo "\[\[ FLOORS  \]\]"
    return $?
}

function fetch_state_file_room_start_pattern () {
    echo "\[\[ ROOMS   \]\]"
    return $?
}

function fetch_state_file_client_start_pattern () {
    echo "\[\[ CLIENTS \]\]"
    return $?
}

function fetch_state_file_guest_start_pattern () {
    echo "\[\[ GUESTS  \]\]"
    return $?
}

function fetch_state_file_stop_pattern () {
    echo "\[\[ _______ \]\]"
    return $?
}


