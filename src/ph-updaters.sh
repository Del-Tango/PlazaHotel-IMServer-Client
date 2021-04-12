#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# UPDATERS

function update_explorer_details () {
    local ROOM_PORT=$1
    local ALIAS="$2"
    local GUEST_OF="$3"
    local ROOM_NUMBER=$4
    local FLOOR_LEVEL=$5
    local ACCESS_KEY="$6"
    debug_msg "Updating explorer details (${MAGENTA}$ROOM_PORT,$ALIAS,"\
        "$ROOM_NUMBER,$FLOOR_LEVEL,`echo $ACCESS_KEY | md5sum`${RESET})..."
    set_room_port_number $ROOM_PORT
    set_alias "$ALIAS"
    set_guest_of_alias "$GUEST_OF"
    set_target_room_number $ROOM_NUMBER
    set_target_floor_number $FLOOR_LEVEL
    set_floor_access_key "$ACCESS_KEY"
    return 0
}

function update_guest_details () {
    local ALIAS="$1"
    local GUEST_OF="$2"
    local ROOM_NUMBER=$3
    local ROOM_PORT=$4
    local FLOOR_LEVEL=$5
    debug_msg "Updating guest details (${MAGENTA}$ROOM_PORT,$ALIAS,$GUEST_OF"\
        "$ROOM_NUMBER,$FLOOR_LEVEL${RESET})..."
    set_room_port_number $ROOM_PORT
    set_alias "$ALIAS"
    set_guest_of_alias "$GUEST_OF"
    set_target_room_number $ROOM_NUMBER
    set_target_floor_number $FLOOR_LEVEL
    return 0
}

function update_client_details () {
    local ROOM_PORT=$1
    local ALIAS="$2"
    local GUEST_LIST="$3"
    local ROOM_NUMBER=$4
    local FLOOR_LEVEL=$5
    local ACCESS_KEY="$6"
    debug_msg "Updating client details (${MAGENTA}$ROOM_PORT,$ALIAS,$GUEST_LIST"\
        "$ROOM_NUMBER,$FLOOR_LEVEL,`echo $ACCESS_KEY | md5sum`${RESET})..."
    set_room_port_number $ROOM_PORT
    set_alias "$ALIAS"
    set_guest_list "$GUEST_LIST"
    set_target_room_number $ROOM_NUMBER
    set_target_floor_number $FLOOR_LEVEL
    set_floor_access_key "$ACCESS_KEY"
    return 0
}

function update_server_state_cache () {
    send_plaza_hotel_state_file_update_signal
    sleep 0.2
    parse_state_file "${MD_DEFAULT['state-file']}"
    return $?
}

