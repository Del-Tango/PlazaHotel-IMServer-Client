#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# DISPLAY

function display_loading_message () {
    local WAIT_SECONDS=$1
    local LOADING_STRING="$2"
    local PREVIOUS='-'
    ITERCOUNT=`echo "$WAIT_SECONDS * 2" | bc`
    for item in `seq $ITERCOUNT`; do
        local MESSAGE_STRING=""
        case "$PREVIOUS" in
            '/')
                local PREVIOUS='-'
                ;;
            '-')
                local PREVIOUS='\'
                ;;
            '\')
                local PREVIOUS='/'
                ;;
        esac
        local MESSAGE_STRING="${LOADING_STRING}($PREVIOUS)"
        clear; echo "$MESSAGE_STRING"; sleep 0.5
    done
    return 0
}

function display_plaza_hotel_available_rooms () {
    STATE_ROOM_LINES=( $@ )
    if [ ${#STATE_ROOM_LINES[@]} -eq 0 ]; then
        return 1
    fi
    echo; info_msg "Available (${BLUE}$SCRIPT_NAME${RESET}) rooms -
    "
    for room_line in ${STATE_ROOM_LINES[@]}; do
        ROOM_NUMBER=`filter_room_number_from_state_line "$room_line"`
        FLOOR_LEVEL=`filter_room_floor_level_from_state_line "$room_line"`
        TIMESTAMP=`filter_room_timestamp_from_state_line "$room_line"`
#       PORT_NUMBER=`filter_room_port_number_from_state_line "$room_line"`
        CAPACITY=`filter_room_capacity_from_state_line "$room_line"`
        CORTEX_TYPE=`filter_room_cortex_type_from_state_line "$room_line"`
        CLIENT_ALIAS=`filter_room_client_alias_from_state_line "$room_line"`
        GUEST_LIST=`filter_room_guest_list_from_state_line "$room_line"`
        if [ -z "$CLIENT_ALIAS" ]; then
            BOOKED_FLAG="${GREEN}Vacant${RESET}"
        else
            BOOKED_FLAG="${RED}Booked${RESET}"
        fi
        echo "${MAGENTA}$FLOOR_TIMESTAMP${RESET} -"\
            "${CYAN}Room Number${RESET} (${WHITE}$ROOM_NUMBER${RESET}) -"\
            "$BOOKED_FLAG,"\
            "${GREEN}$CORTEX_TYPE${RESET} -"\
            "${CYAN}capacity of${RESET} (${WHITE}$CAPACITY${RESET})"\
            "${CYAN}orbitals${RESET}"
    done
    return 0
}

function display_plaza_hotel_available_floors () {
    STATE_FLOOR_LINES=( $@ )
    if [ ${#STATE_FLOOR_LINES[@]} -eq 0 ]; then
        return 1
    fi
    info_msg "Available (${BLUE}$SCRIPT_NAME${RESET}) floors -
    "
    for floor_line in ${STATE_FLOOR_LINES[@]}; do
        FLOOR_LEVEL=`filter_floor_number_from_state_line "$floor_line"`
        FLOOR_TIMESTAMP=`filter_floor_timestamp_from_state_line "$floor_line"`
        FLOOR_ROOM_COUNT=`filter_floor_room_count_from_state_line "$floor_line"`
        FLOOR_USER_COUNT=`filter_floor_user_count_from_state_line "$floor_line"`
        FLOOR_PROTECTED_FLAG=`filter_floor_protected_flag_from_state_line "$floor_line"`
        echo "${MAGENTA}$FLOOR_TIMESTAMP${RESET} -"\
            "${CYAN}Floor Level${RESET} (${WHITE}$FLOOR_LEVEL${RESET}) -"\
            "${GREEN}$FLOOR_PROTECTED_FLAG${RESET} -"\
            "(${WHITE}$FLOOR_ROOM_COUNT${RESET}) ${CYAN}active rooms${RESET},"\
            "(${WHITE}$FLOOR_USER_COUNT${RESET}) ${CYAN}orbitals online${RESET}"
    done
    return 0
}

function display_im_server_loading_message () {
    local LOADING_STRING="[ LOADING ]: Plaza Hotel IM Server... "
    display_loading_message 4 "$LOADING_STRING"
    return $?
}

function display_im_client_loading_message () {
    local LOADING_STRING="[ LOADING ]: Plaza Hotel IM Client... "
    display_loading_message 4 "$LOADING_STRING"
    return $?
}

function display_client_banner_file () {
    local CLEAR_SCREEN=${1:-clear-screen-on}
    cat "${MD_DEFAULT['client-banner-file']}" > "${MD_DEFAULT['tmp-file']}"
    case "$CLEAR_SCREEN" in
        'clear-screen-on')
            clear
            ;;
    esac; echo "${RED} `cat ${MD_DEFAULT['tmp-file']}` ${RESET}"
    return 0
}

function display_plaza_hotel_banner () {
    local CLEAR_SCREEN=${1:-clear-screen-on}
    display_script_banner "$CLEAR_SCREEN"
    return $?
}

function display_formatted_settings () {
    display_formatted_setting_conf_file
    display_formatted_setting_log_file
    display_formatted_setting_temporary_file
    display_formatted_setting_server_state_file_path
    display_formatted_setting_server_key_file_path
    display_formatted_setting_server_state_fifo_path
    display_formatted_setting_server_response_fifo_path
    display_formatted_setting_system_user_name
    display_formatted_setting_server_address
    display_formatted_setting_port_number
    display_formatted_setting_target_hotel_floor_count
    display_formatted_setting_target_hotel_room_count
    display_formatted_setting_client_alias
    display_formatted_setting_client_category_type
    display_formatted_setting_client_action
    display_formatted_setting_client_guest_list
    display_formatted_setting_guest_of_client_alias
    display_formatted_setting_hotel_floor_access_key
    display_formatted_setting_target_hotel_floor_level
    display_formatted_setting_target_hotel_room_number
    display_formatted_setting_room_capacity
    display_formatted_setting_room_buffer_size
    display_formatted_setting_log_lines
    display_formatted_setting_silent
    display_formatted_setting_safety
    return 0
}

function display_plaza_hotel_settings () {
    display_formatted_settings | column
    echo; return 0
}

# GENERAL

function display_formatted_setting_target_hotel_floor_count () {
    echo "[ ${CYAN}Hotel Height${RESET}        ]: ${WHITE}${MD_DEFAULT['floor-count']:-${RED}Unspecified}${RESET} floors"
    return $?
}

function display_formatted_setting_target_hotel_room_count () {
    echo "[ ${CYAN}Hotel Width${RESET}         ]: ${WHITE}${MD_DEFAULT['room-count']:-${RED}Unspecified}${RESET} rooms"
    return $?
}

function display_formatted_setting_server_state_file_path () {
    echo "[ ${CYAN}Server State File${RESET}   ]: ${YELLOW}${MD_DEFAULT['state-file']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_server_state_fifo_path () {
    echo "[ ${CYAN}Server State Pipe${RESET}   ]: ${MAGENTA}${MD_DEFAULT['state-fifo']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_server_response_fifo_path () {
    echo "[ ${CYAN}Server Resp Pipe${RESET}    ]: ${MAGENTA}${MD_DEFAULT['response-fifo']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_room_buffer_size () {
    echo "[ ${CYAN}Room Buffer Size${RESET}    ]: ${WHITE}${MD_DEFAULT['buffer-size']:-${RED}Unspecified}${RESET} bytes"
    return $?
}

function display_formatted_setting_port_number () {
    echo "[ ${CYAN}Port Number${RESET}         ]: ${WHITE}${MD_DEFAULT['port-number']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_server_address () {
    echo "[ ${CYAN}Server Address${RESET}      ]: ${MAGENTA}${MD_DEFAULT['address']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_safety () {
    echo "[ ${CYAN}Safety${RESET}              ]: `format_flag_colors $MD_SAFETY`"
    return $?
}

function display_formatted_setting_conf_file () {
    echo "[ ${CYAN}Conf File${RESET}           ]: ${YELLOW}${MD_DEFAULT['conf-file']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_log_file () {
    echo "[ ${CYAN}Log File${RESET}            ]: ${YELLOW}${MD_DEFAULT['log-file']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_temporary_file () {
    echo "[ ${CYAN}Temporary File${RESET}      ]: ${YELLOW}${MD_DEFAULT['tmp-file']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_log_lines () {
    echo "[ ${CYAN}Log Lines${RESET}           ]: ${WHITE}${MD_DEFAULT['log-lines']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_silent () {
    echo "[ ${CYAN}Silent${RESET}              ]: `format_flag_colors ${MD_DEFAULT['silent']}`"
    return $?
}

# SERVER SPECIFIC

function display_formatted_setting_system_user_name () {
    echo "[ ${CYAN}System User${RESET}         ]: ${YELLOW}${MD_DEFAULT['system-user']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_server_key_file_path () {
    echo "[ ${CYAN}Server Key File${RESET}     ]: ${YELLOW}${MD_DEFAULT['key-file']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_room_capacity () {
    echo "[ ${CYAN}Hotel Room Capacity${RESET} ]: ${WHITE}${MD_DEFAULT['room-capacity']:-${RED}Unspecified}${RESET} users"
    return $?
}

# CLIENT SPECIFIC

function display_formatted_setting_client_alias () {
    echo "[ ${CYAN}Client Alias${RESET}        ]: ${GREEN}${MD_DEFAULT['alias']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_client_category_type () {
    echo "[ ${CYAN}Client Type${RESET}         ]: ${MAGENTA}${MD_DEFAULT['client-type']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_client_action () {
    echo "[ ${CYAN}Client Action${RESET}       ]: ${MAGENTA}${MD_DEFAULT['client-action']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_client_guest_list () {
    if [[ "${MD_DEFAULT['client-type']}" != 'client' ]]; then
        return 1
    fi
    echo "[ ${CYAN}Guest List${RESET}          ]: ${GREEN}${MD_DEFAULT['guest-list']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_target_hotel_floor_level () {
    echo "[ ${CYAN}Floor Level${RESET}         ]: ${WHITE}${MD_DEFAULT['floor-level']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_target_hotel_room_number () {
    echo "[ ${CYAN}Room Number${RESET}         ]: ${WHITE}${MD_DEFAULT['room-number']:-${RED}Unspecified}${RESET}"
    return $?
}

function display_formatted_setting_hotel_floor_access_key () {
    echo "[ ${CYAN}Floor Access Key${RESET}    ]: ${GREEN}${MD_DEFAULT['access-key']:-${RED}Unspecified}${RESET}"
    return $?
}

# GUEST SPECIFIC

function display_formatted_setting_guest_of_client_alias () {
    if [[ "${MD_DEFAULT['client-type']}" != 'guest' ]]; then
        return 1
    fi
    echo "[ ${CYAN}Guest Of${RESET}            ]: ${GREEN}${MD_DEFAULT['guest-of']:-${RED}Unspecified}${RESET}"
    return $?
}

