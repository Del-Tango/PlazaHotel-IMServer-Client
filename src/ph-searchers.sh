#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# SEARCHERS

function search_room_number_by_client_alias () {
    local CLIENT_ALIAS="$1"
    CLIENTS_BOOKED=( `fetch_server_state_cached_client_lines` )
    for state_line in ${CLIENTS_BOOKED[@]}; do
        CURRENT_CLIENT=`filter_client_alias_from_state_line "$state_line"`
        if [[ "$CLIENT_ALIAS" != "$CURRENT_CLIENT" ]]; then
            continue
        fi
        ROOM_NUMBER=`filter_client_booked_room_number_from_state_line "$state_line"`
        echo $ROOM_NUMBER
        return $?
    done
    return 1
}

function search_client_guest_list_by_alias () {
    local CLIENT_ALIAS="$1"
    CLIENTS_BOOKED=( `fetch_server_state_cached_client_lines` )
    for state_line in ${CLIENTS_BOOKED[@]}; do
        CURRENT_CLIENT=`filter_client_alias_from_state_line "$state_line"`
        if [[ "$CLIENT_ALIAS" != "$CURRENT_CLIENT" ]]; then
            continue
        fi
        GUEST_LIST=( `filter_client_guest_list_from_state_line "$state_line"` )
        echo ${GUEST_LIST[@]}
        return $?
    done
    return 1
}

function search_room_port_number () {
    local ROOM_NUMBER=$1
    AVAILABLE_ROOMS=( `fetch_server_state_cached_room_lines` )
    for state_line in ${AVAILABLE_ROOMS[@]}; do
        CURRENT_ROOM=`filter_room_number_from_state_line "$state_line"`
        if [[ "$ROOM_NUMBER" != "$CURRENT_ROOM" ]]; then
            continue
        fi
        ROOM_PORT_NUMBER=`filter_room_port_number_from_state_line "$state_line"`
        echo $ROOM_PORT_NUMBER
        return $?
    done
    return 1
}

function search_room_floor_level () {
    local ROOM_NUMBER=$1
    AVAILABLE_ROOMS=( `fetch_server_state_cached_room_lines` )
    for state_line in ${AVAILABLE_ROOMS[@]}; do
        CURRENT_ROOM=`filter_room_number_from_state_line "$state_line"`
        if [[ "$ROOM_NUMBER" != "$CURRENT_ROOM" ]]; then
            continue
        fi
        FLOOR_LEVEL=`filter_room_floor_level_from_state_line "$state_line"`
        echo $FLOOR_LEVEL
        return $?
    done
    return 1
}

function search_checked_in_client_alias_by_room_number () {
    local ROOM_NUMBER=$1
    AVAILABLE_ROOMS=( `fetch_server_state_cached_room_lines` )
    for state_line in ${AVAILABLE_ROOMS[@]}; do
        CURRENT_ROOM=`filter_room_number_from_state_line "$state_line"`
        if [[ "$ROOM_NUMBER" != "$CURRENT_ROOM" ]]; then
            continue
        fi
        CLIENT_ALIAS=`filter_room_client_alias_from_state_line "$state_line"`
        echo "$CLIENT_ALIAS"
        return $?
    done
    return 1
}

function search_floor_protected_flag_by_level () {
    local FLOOR_LEVEL=$1
    AVAILABLE_FLOORS=( `fetch_server_state_cached_floor_lines` )
    for state_line in ${AVAILABLE_FLOORS[@]}; do
        CURRENT_LEVEL=`filter_floor_number_from_state_line "$state_line"`
        if [[ "$FLOOR_LEVEL" != "$CURRENT_LEVEL" ]]; then
            continue
        fi
        PROTECTED_FLAG=`filter_floor_protected_flag_from_state_line "$state_line"`
        echo "$PROTECTED_FLAG"
        return $?
    done
    return 1
}
