#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# CHECKERS

function check_room_is_booked () {
    local ROOM_NUMBER=$1
    local FLOOR_LEVEL=$2
    AVAILABLE_ROOMS=( `fetch_server_state_cached_room_lines` )
    FILTERED_ROOMS=( `filter_server_state_cached_room_lines_for_floor $FLOOR_LEVEL` )
    for state_line in ${FILTERED_ROOMS[@]}; do
        CURRENT_ROOM=`filter_room_number_from_state_line "$state_line"`
        if [[ "$CURRENT_ROOM" != "$ROOM_NUMBER" ]]; then
            continue
        fi
        CLIENT_ALIAS=`filter_room_client_alias_from_state_line "$state_line"`
        if [ ! -z "$CLIENT_ALIAS" ]; then
            return 0
        fi; return 1
    done
    return 2
}

function check_client_room_explore () {
    local ROOM_NUMBER=$1
    local FLOOR_NUMBER=$2
    AVAILABLE_ROOMS=( `` )
    check_is_valid_room_number $ROOM_NUMBER $FLOOR_NUMBER
    if [ $? -ne 0 ]; then
        return 1
    fi
    check_room_is_booked $ROOM_NUMBER $FLOOR_NUMBER
    if [ $? -ne 0 ]; then
        return 2
    fi
    check_room_is_open_cortex $ROOM_NUMBER $FLOOR_NUMBER
    if [ $? -ne 0 ]; then
        return 3
    fi
    return 0
}

function check_is_valid_client_alias () {
    local CLIENT_ALIAS=$1
    CLIENTS_BOOKED=( `fetch_server_state_cached_client_lines` )
    for state_line in ${CLIENTS_BOOKED[@]}; do
        CURRENT_CLIENT=`filter_client_alias_from_state_line "$state_line"`
        if [[ "$CURRENT_CLIENT" == "$CLIENT_ALIAS" ]]; then
            return 0
        fi
    done
    return 1
}

function check_is_vacant_room_number () {
    local ROOM_NUMBER=$1
    CLIENT_ALIAS=`search_checked_in_client_alias_by_room_number $ROOM_NUMBER`
    if [ ! -z "$CLIENT_ALIAS" ]; then
        return 1
    fi
    return 0
}

function check_is_valid_room_number () {
    local ROOM_NUMBER=$1
    local FLOOR_LEVEL=$2
    AVAILABLE_ROOMS=( `fetch_server_state_cached_room_lines` )
    FILTERED_ROOMS=( `filter_server_state_cached_room_lines_for_floor $FLOOR_LEVEL` )
    for state_line in ${FILTERED_ROOMS[@]}; do
        CURRENT_ROOM=`filter_room_number_from_state_line "$state_line"`
        if [[ "$CURRENT_ROOM" == "$ROOM_NUMBER" ]]; then
            return 0
        fi
    done
    return 1
}

function check_is_valid_floor_level () {
    local FLOOR_LEVEL=$1
    AVAILABLE_FLOORS=( `fetch_server_state_cached_floor_lines` )
    for state_line in ${AVAILABLE_FLOORS[@]}; do
        FLOOR_NUMBER=`filter_floor_number_from_state_line "$state_line"`
        if [[ "$FLOOR_NUMBER" == "$FLOOR_LEVEL" ]]; then
            return 0
        fi
    done
    return 1
}

function check_client_room_checkin () {
    local ROOM_NUMBER=$1
    local FLOOR_NUMBER=$2
    AVAILABLE_ROOMS=( `` )
    check_is_valid_room_number $ROOM_NUMBER $FLOOR_NUMBER
    if [ $? -ne 0 ]; then
        return 1
    fi
    check_is_vacant_room_number $ROOM_NUMBER
    if [ $? -ne 0 ]; then
        return 2
    fi
    return 0
}

function check_client_room_explore () {
    local ROOM_NUMBER=$1
    local FLOOR_NUMBER=$2
    AVAILABLE_ROOMS=( `` )
    check_is_valid_room_number $ROOM_NUMBER $FLOOR_NUMBER
    if [ $? -ne 0 ]; then
        return 1
    fi
    check_room_is_booked $ROOM_NUMBER $FLOOR_NUMBER
    if [ $? -ne 0 ]; then
        return 2
    fi
    check_room_is_open_cortex $ROOM_NUMBER $FLOOR_NUMBER
    if [ $? -ne 0 ]; then
        return 3
    fi
    return 0
}

function check_room_is_open_cortex () {
    local ROOM_NUMBER=$1
    local FLOOR_LEVEL=$2
    AVAILABLE_ROOMS=( `fetch_server_state_cached_room_lines` )
    FILTERED_ROOMS=( `filter_server_state_cached_room_lines_for_floor $FLOOR_LEVEL` )
    for state_line in ${FILTERED_ROOMS[@]}; do
        CURRENT_ROOM=`filter_room_number_from_state_line "$state_line"`
        if [[ "$CURRENT_ROOM" != "$ROOM_NUMBER" ]]; then
            continue
        fi
        CORTEX_TYPE=`filter_room_cortex_type_from_state_line "$state_line"`
        if [[ "$CORTEX_TYPE" == 'open-cortex' ]]; then
            return 0
        fi; return 1
    done
    return 2
}

function check_guest_is_on_the_list () {
    local GUEST_ALIAS="$1"
    local CLIENT_ALIAS="$2"
    GUEST_LIST=( `search_client_guest_list_by_alias "$CLIENT_ALIAS"` )
    for alias in ${GUEST_LIST[@]}; do
        if [[ "$GUEST_ALIAS" == "$alias" ]]; then
            return 0
        fi
    done
    return 1
}

