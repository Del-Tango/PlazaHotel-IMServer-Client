#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# FILTERS

function filter_server_state_cached_room_lines_for_floor () {
    local FLOOR_LEVEL=$1
    AVAILABLE_ROOMS=( `fetch_server_state_cached_room_lines` )
    debug_msg "Floor level (${WHITE}$FLOOR_LEVEL${RESET})"
    debug_msg "Available rooms (${MAGENTA}${AVAILABLE_ROOMS[@]}${RESET})"
    FLOOR_ROOMS=()
    for state_line in ${AVAILABLE_ROOMS[@]}; do
        ROOM_FLOOR=`filter_room_floor_level_from_state_line "$state_line"`
        debug_msg "Room Floor (${WHITE}$ROOM_FLOOR${RESET})"
        if [[ "$ROOM_FLOOR" != "$FLOOR_LEVEL" ]]; then
            continue
        fi
        FLOOR_ROOMS=( ${FLOOR_ROOMS[@]} "$state_line" )
    done
    echo ${FLOOR_ROOMS[@]}
    return $?
}

# SERVER STATE FLOOR VALUE FILTER

function filter_floor_number_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 1
    return $?
}

function filter_floor_timestamp_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 2
    return $?
}

function filter_floor_room_count_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 3
    return $?
}

function filter_floor_user_count_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 4
    return $?
}

function filter_floor_protected_flag_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 5
    return $?
}

# SERVER STATE ROOM VALUE FILTER

function filter_room_number_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 1
    return $?
}

function filter_room_floor_level_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 3
    return $?
}

function filter_room_timestamp_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 2
    return $?
}

function filter_room_port_number_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 4
    return $?
}

function filter_room_capacity_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 5
    return $?
}

function filter_room_cortex_type_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 6
    return $?
}

function filter_room_client_alias_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 7
    return $?
}

function filter_room_guest_list_from_state_line () {
    local STATE_FILE_LINE="$1"
    GUEST_LIST=()
    CURRENT_GUEST_INDEX=8
    while :
    do
        GUEST_ALIAS=`echo "$STATE_FILE_LINE" | cut -d ',' -f $CURRENT_GUEST_INDEX`
        if [ -z $GUEST_ALIAS ]; then
            break
        fi
        GUEST_LIST=( ${GUEST_LIST[@]} "$GUEST_ALIAS" )
        CURRENT_GUEST_INDEX=$((CURRENT_GUEST_INDEX + 1))
    done
    echo "${GUEST_LIST[@]}"
    return $?
}

# SERVER STATE CLIENT VALUE FILTER

function filter_client_alias_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 1
    return $?
}

function filter_client_timestamp_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 2
    return $?
}

function filter_client_booked_room_number_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 3
    return $?
}

function filter_client_booked_floor_level_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 4
    return $?
}

function filter_client_guest_count_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 5
    return $?
}

function filter_client_guest_list_from_state_line () {
    local STATE_FILE_LINE="$1"
    GUEST_LIST=()
    CURRENT_GUEST_INDEX=6
    while :
    do
        GUEST_ALIAS=`echo "$STATE_FILE_LINE" | cut -d ',' -f $CURRENT_GUEST_INDEX`
        if [ -z $GUEST_ALIAS ]; then
            break
        fi
        GUEST_LIST=( ${GUEST_LIST[@]} "$GUEST_ALIAS" )
        CURRENT_GUEST_INDEX=$((CURRENT_GUEST_INDEX + 1))
    done
    echo "${GUEST_LIST[@]}"
    return $?
}

# SERVER STATE GUEST VALUE FILTER

function filter_guest_alias_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 1
    return $?
}

function filter_guest_timestamp_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 2
    return $?
}

function filter_guest_of_client_alias_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 3
    return $?
}

function filter_guest_room_number_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 4
    return $?
}

function filter_guest_floor_level_from_state_line () {
    local STATE_FILE_LINE="$1"
    echo "$STATE_FILE_LINE" | cut -d ',' -f 5
    return $?
}


