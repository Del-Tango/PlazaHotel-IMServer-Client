#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# PARSERS

function parse_server_state_floors () {
    local SERVER_STATE_FILE="$1"
    START_PATTERN=`fetch_state_file_floor_start_pattern`
    STOP_PATTERN=`fetch_state_file_stop_pattern`
    FILE_LINES=`filter_file_content "$SERVER_STATE_FILE" "$START_PATTERN" "$STOP_PATTERN"`
    SANITIZED_FILE_LINES=`echo "$FILE_LINES" | grep -v '\[\[' | grep -v '^$' | grep -v '^#'`
    set_server_state_floors "$SANITIZED_FILE_LINES"
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo; nok_msg "Something went wrong."\
            "Could not set server state floor lines: \n\n"\
            "${RED}$SANITIZED_FILE_LINES${RESET}."
    fi
    return $EXIT_CODE
}

function parse_server_state_rooms () {
    local SERVER_STATE_FILE="$1"
    START_PATTERN=`fetch_state_file_room_start_pattern`
    STOP_PATTERN=`fetch_state_file_stop_pattern`
    FILE_LINES=`filter_file_content "$SERVER_STATE_FILE" "$START_PATTERN" "$STOP_PATTERN"`
    SANITIZED_FILE_LINES=`echo "$FILE_LINES" | grep -v '\[\[' | grep -v '^$' | grep -v '^#'`
    set_server_state_rooms "$SANITIZED_FILE_LINES"
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo; nok_msg "Something went wrong."\
            "Could not set server state room lines: \n\n"\
            "${RED}$SANITIZED_FILE_LINES${RESET}."
    fi
    return $EXIT_CODE
}

function parse_server_state_clients () {
    local SERVER_STATE_FILE="$1"
    START_PATTERN=`fetch_state_file_client_start_pattern`
    STOP_PATTERN=`fetch_state_file_stop_pattern`
    FILE_LINES=`filter_file_content "$SERVER_STATE_FILE" "$START_PATTERN" "$STOP_PATTERN"`
    SANITIZED_FILE_LINES=`echo "$FILE_LINES" | grep -v '\[\[' | grep -v '^$' | grep -v '^#'`
    set_server_state_clients "$SANITIZED_FILE_LINES"
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo; nok_msg "Something went wrong."\
            "Could not set server state client lines: \n\n"\
            "${RED}$SANITIZED_FILE_LINES${RESET}."
    fi
    return $EXIT_CODE
}

function parse_server_state_guests () {
    local SERVER_STATE_FILE="$1"
    START_PATTERN=`fetch_state_file_guest_start_pattern`
    STOP_PATTERN=`fetch_state_file_stop_pattern`
    FILE_LINES=`filter_file_content "$SERVER_STATE_FILE" "$START_PATTERN" "$STOP_PATTERN"`
    SANITIZED_FILE_LINES=`echo "$FILE_LINES" | grep -v '\[\[' | grep -v '^$' | grep -v '^#'`
    set_server_state_guests "$SANITIZED_FILE_LINES"
    EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        echo; nok_msg "Something went wrong."\
            "Could not set server state guest lines: \n\n"\
            "${RED}$SANITIZED_FILE_LINES${RESET}."
    fi
    return $EXIT_CODE
}

function parse_state_file () {
    local SERVER_STATE_FILE="$1"
    parse_server_state_floors "$SERVER_STATE_FILE"
    parse_server_state_rooms "$SERVER_STATE_FILE"
    parse_server_state_clients "$SERVER_STATE_FILE"
    parse_server_state_guests "$SERVER_STATE_FILE"
    return 0
}

# MISCELLANEOUS

