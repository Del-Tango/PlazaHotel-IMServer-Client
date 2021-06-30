#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# ACTIONS

function action_purge_system_user () {
    echo; check_privileged_access
    if [ $? -ne 0 ]; then
        warning_msg "${RED}System user purge requires"\
            "SuperUser privileges!${RESET}"\
            "Try running (${YELLOW}$0${RESET}) as ${RED}root${RESET}."
        return 0
    fi
    check_safety_off
    if [ $? -ne 0 ]; then
        warning_msg "${GREEN}$SCRIPT_NAME${RESET} safety is"\
            "(${GREEN}ON${RESET}). System user"\
            "(${YELLOW}${MD_DEFAULT['system-user']}${RESET})"\
            "is not beeing purged."
        return 0
    fi
    local USER_HOME_DIR="/home/${MD_DEFAULT['system-user']}"
    remove_system_user "${MD_DEFAULT['system-user']}"
    if [ $? -ne 0 ]; then
        warning_msg "Something went wrong!"\
            "Could not remove system user"\
            "(${RED}${MD_DEFAULT['system-user']}${RESET})."
        return 0
    fi
    remove_system_group "$SCRIPT_NAME"
    if [ $? -ne 0 ]; then
        warning_msg "Something went wrong!"\
            "Could not remove system group"\
            "(${RED}$SCRIPT_NAME${RESET})."
        return 0
    fi
    remove_directory "$USER_HOME_DIR"
    if [ $? -ne 0 ]; then
        warning_msg "Something went wrong!"\
            "Could not remove system user HOME directory"\
            "(${RED}$USER_HOME_DIR${RESET})."
        return 0
    fi
    done_msg "Teardown complete!"
    info_msg "System User Name      : ${RED}${MD_DEFAULT['system-user']}${RESET}"
    info_msg "System Group Name     : ${RED}$SCRIPT_NAME${RESET}"
    info_msg "Home Directory        : ${RED}$USER_HOME_DIR${RESET}"
    return 0
}

function action_setup_system_user () {
    echo;
    check_privileged_access
    if [ $? -ne 0 ]; then
        warning_msg "${RED}System user setup requires"\
            "SuperUser privileges!${RESET}"\
            "Try running (${YELLOW}$0${RESET}) as ${RED}root${RESET}."
        return 0
    fi
    check_safety_off
    if [ $? -ne 0 ]; then
        warning_msg "${GREEN}$SCRIPT_NAME${RESET} safety is"\
            "(${GREEN}ON${RESET}). System user"\
            "(${YELLOW}${MD_DEFAULT['system-user']}${RESET})"\
            "is not beeing set up."
        return 0
    fi
    create_system_user "${MD_DEFAULT['system-user']}"
    if [ $? -ne 0 ]; then
        warning_msg "Something went wrong!"\
            "Could not create system user"\
            "(${RED}${MD_DEFAULT['system-user']}${RESET})."
        return 0
    fi
    create_system_group "$SCRIPT_NAME" &> /dev/null
    add_system_user_to_group "`whoami`" "$SCRIPT_NAME" &> /dev/null
    add_system_user_to_group "${MD_DEFAULT['system-user']}" "$SCRIPT_NAME"
    if [ $? -ne 0 ]; then
        warning_msg "Something went wrong!"\
            "Could not copy project"\
            "(${RED}${MD_DEFAULT['project-path']}${RESET})"\
            "to system user home directory (${RED}$USER_HOME_DIR${RESET})."
        return 0
    fi
    local USER_HOME_DIR="/home/${MD_DEFAULT['system-user']}"
    cp -r "${MD_DEFAULT['project-path']}" "$USER_HOME_DIR" &> /dev/null
    if [ $? -ne 0 ]; then
        warning_msg "Something went wrong!"\
            "Could not copy project"\
            "(${RED}${MD_DEFAULT['project-path']}${RESET})"\
            "to system user home directory (${RED}$USER_HOME_DIR${RESET})."
        return 0
    fi
    PROJECT_DIR_NAME=`basename ${MD_DEFAULT['project-path']}`
    local USER_PROJECT_PATH="$USER_HOME_DIR/$PROJECT_DIR_NAME"
    local USER_QUICK_INIT_PATH="$USER_PROJECT_PATH/init-client"
    local USER_BASHRC_PATH="$USER_HOME_DIR/.bashrc"
    chown -R "${MD_DEFAULT['system-user']}" "$USER_PROJECT_PATH" &> /dev/null
    chmod +x "$USER_QUICK_INIT_PATH" &> /dev/null
    echo "cd $USER_PROJECT_PATH &> /dev/null" >> "$USER_BASHRC_PATH"
    echo "$USER_QUICK_INIT_PATH" >> "$USER_BASHRC_PATH"
    echo 'logout &> /dev/null' >> "$USER_BASHRC_PATH"
    echo; done_msg "Construction complete!"
    info_msg "System User Name      : ${GREEN}${MD_DEFAULT['system-user']}${RESET}"
    info_msg "System Group Name     : ${CYAN}$SCRIPT_NAME${RESET}"
    info_msg "Home Directory        : ${BLUE}$USER_HOME_DIR${RESET}"
    info_msg "User Project Directory: ${BLUE}$USER_PROJECT_PATH${RESET}"
    info_msg "User BashRC File      : ${YELLOW}$USER_BASHRC_PATH${RESET}"
    info_msg "User Client Init File : ${YELLOW}$USER_QUICK_INIT_PATH${RESET}"
    info_msg "Post Exec Action      : ${MAGENTA}logout &> /dev/null${RESET}"
    return 0
}

function action_plaza_hotel_interactive_client_explore_room () {
    update_server_state_cache
    AVAILABLE_FLOORS=( `fetch_server_state_cached_floor_lines` )
    echo; display_plaza_hotel_available_floors ${AVAILABLE_FLOORS[@]}
    echo; info_msg "Type desired floor level or (${MAGENTA}.back${RESET}) -"
    FLOOR_LEVEL=`fetch_floor_level_from_user`
    if [ $? -ne 0 ]; then return 0; fi
    PROTECTED_FLAG=`search_floor_protected_flag_by_level $FLOOR_LEVEL`
    if [[ "$PROTECTED_FLAG" == 'protected' ]]; then
        echo; info_msg "Type floor level access key or (${MAGENTA}.back${RESET}) -"
        FLOOR_ACCESS_KEY=`fetch_floor_access_key_from_user`
        if [ $? -ne 0 ]; then return 0; fi
    fi
    AVAILABLE_ROOMS=( `fetch_server_state_cached_room_lines` )
    FILTERED_ROOMS=( `filter_server_state_cached_room_lines_for_floor $FLOOR_LEVEL` )
    display_plaza_hotel_available_rooms ${FILTERED_ROOMS[@]}
    echo; info_msg "Type desired ${GREEN}open-cortex${RESET} room number"\
        "or (${MAGENTA}.back${RESET}) -"
    ROOM_NUMBER=`fetch_explore_room_number_from_user $FLOOR_LEVEL`
    if [ $? -ne 0 ]; then return 0; fi
    ROOM_PORT=`search_room_port_number $ROOM_NUMBER`
    echo; info_msg "Type your orbital alias or (${MAGENTA}.back${RESET}) -"
    ALIAS=`fetch_data_from_user 'Alias'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    BOOKED_CLIENT=`search_checked_in_client_alias_by_room_number $ROOM_NUMBER`
    update_explorer_details $ROOM_PORT "$ALIAS" "$BOOKED_CLIENT" $ROOM_NUMBER \
        $FLOOR_LEVEL "$FLOOR_ACCESS_KEY"
    action_plaza_hotel_client_explore_room
    return $?
}

function action_plaza_hotel_interactive_guest_join_room () {
    update_server_state_cache
    echo; info_msg "Type your orbital alias or (${MAGENTA}.back${RESET}) -"
    ALIAS=`fetch_data_from_user 'Alias'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    echo; info_msg "Tell us $ALIAS, who is expecting you?"
    while :
    do
        GUEST_OF=`fetch_data_from_user 'GuestOf'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_is_valid_client_alias "$GUEST_OF"
        if [ $? -ne 0 ]; then
            echo; warning_msg "Can't help you, we haven't heard of"\
                "(${RED}$GUEST_OF${RESET})."
            echo; continue
        fi
        check_guest_is_on_the_list "$ALIAS" "$GUEST_OF"
        if [ $? -ne 0 ]; then
            echo; warning_msg "You're not on the guest list of"\
                "(${RED}$GUEST_OF${RESET})."
            echo; continue
        fi; break
    done
    ROOM_NUMBER=`search_room_number_by_client_alias "$GUEST_OF"`
    ROOM_PORT=`search_room_port_number $ROOM_NUMBER`
    FLOOR_LEVEL=`search_room_floor_level $ROOM_NUMBER`
    update_guest_details "$ALIAS" "$GUEST_OF" $ROOM_NUMBER $ROOM_PORT \
        $FLOOR_LEVEL
    action_plaza_hotel_guest_join_room
    return $?
}

function action_plaza_hotel_interactive_client_book_room () {
    update_server_state_cache
    AVAILABLE_FLOORS=( `fetch_server_state_cached_floor_lines` )
    echo; display_plaza_hotel_available_floors ${AVAILABLE_FLOORS[@]}
    echo; info_msg "Type desired floor level or (${MAGENTA}.back${RESET}) -"
    FLOOR_LEVEL=`fetch_floor_level_from_user`
    if [ $? -ne 0 ]; then return 0; fi
    PROTECTED_FLAG=`search_floor_protected_flag_by_level $FLOOR_LEVEL`
    if [[ "$PROTECTED_FLAG" == 'protected' ]]; then
        echo; info_msg "Type floor level access key or (${MAGENTA}.back${RESET}) -"
        FLOOR_ACCESS_KEY=`fetch_floor_access_key_from_user`
        if [ $? -ne 0 ]; then return 0; fi
    fi
    AVAILABLE_ROOMS=( `fetch_server_state_cached_room_lines` )
    FILTERED_ROOMS=( `filter_server_state_cached_room_lines_for_floor $FLOOR_LEVEL` )
    display_plaza_hotel_available_rooms ${FILTERED_ROOMS[@]}
    echo; info_msg "Type desired vacant room number or (${MAGENTA}.back${RESET}) -"
    ROOM_NUMBER=`fetch_checkin_room_number_from_user $FLOOR_LEVEL`
    if [ $? -ne 0 ]; then return 0; fi
    echo; info_msg "Type guest list as comma separated aliases"\
        "or (${MAGENTA}.back${RESET}) -"
    info_msg "Setting the guest list to (${MAGENTA}-${RESET}) will make the"\
        "room (${GREEN}open-cortex${RESET})."
    info_msg "${GREEN}OpenCortex${RESET} rooms allow anyone with floor level"\
        "access to join as a client orbital."
    symbol_msg "${BLUE}EXAMPLE${RESET}" \
        "${GREEN}GhostOrbital1,GhostOrbital2,GhostOrbital3${RESET}..."\
        "or ${GREEN}-${RESET}"
    GUEST_LIST=`fetch_data_from_user 'GuestList'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    if [[ "$GUEST_LIST" == '-' ]]; then
        GUEST_LIST=''
    fi
    ROOM_PORT=`search_room_port_number $ROOM_NUMBER`
    echo; info_msg "Type your orbital alias or (${MAGENTA}.back${RESET}) -"
    ALIAS=`fetch_data_from_user 'Alias'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    update_client_details $ROOM_PORT "$ALIAS" "$GUEST_LIST" $ROOM_NUMBER \
        $FLOOR_LEVEL "$FLOOR_ACCESS_KEY"
    action_plaza_hotel_client_book_room
    return $?
}

function action_plaza_hotel_client_explore_room () {
    ARGUMENTS=( `format_plaza_hotel_client_explore_arguments` )
    debug_msg "Client network (${BLUE}$SCRIPT_NAME${RESET}) arguments"\
        "(${MAGENTA}${ARGUMENTS[@]}${RESET})"
    ${PH_CARGO['plaza-hotel']} ${ARGUMENTS[@]}
    return $?
}

function action_plaza_hotel_guest_join_room () {
    ARGUMENTS=( `format_plaza_hotel_guest_join_arguments` )
    debug_msg "Guest join (${BLUE}$SCRIPT_NAME${RESET}) arguments"\
        "(${MAGENTA}${ARGUMENTS[@]}${RESET})"
    ${PH_CARGO['plaza-hotel']} ${ARGUMENTS[@]}
    return $?
}

function action_plaza_hotel_client_book_room () {
    ARGUMENTS=( `format_plaza_hotel_client_checkin_arguments` )
    debug_msg "Client checkin (${BLUE}$SCRIPT_NAME${RESET}) arguments"\
        "(${MAGENTA}${ARGUMENTS[@]}${RESET})"
    ${PH_CARGO['plaza-hotel']} ${ARGUMENTS[@]}
    return $?
}

function action_start_plaza_hotel_server () {
    ARGUMENTS=( `format_plaza_hotel_server_arguments $@` )
    debug_msg "Start server (${BLUE}$SCRIPT_NAME${RESET}) arguments"\
        "(${MAGENTA}${ARGUMENTS[@]}${RESET})"
    ${PH_CARGO['plaza-hotel']} ${ARGUMENTS[@]}
    return $?
}

function action_set_client_action () {
    echo; info_msg "Specify client action or (${MAGENTA}.back${RESET}).
    "
    CLIENT_ACTION=`fetch_selection_from_user 'ClientAction' 'check-in' 'join'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 1
    fi
    set_client_action "$CLIENT_ACTION"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set client action (${RED}$CLIENT_ACTION${RESET})."
    else
        ok_msg "Successfully set client action (${GREEN}$CLIENT_ACTION${RESET})."
    fi
    case "$CLIENT_ACTION" in
        'check-in')
            local CLIENT_TYPE='client'
            ;;
        'join')
            local CLIENT_TYPE='guest'
            ;;
    esac
    set_client_category_type "$CLIENT_TYPE"
    return $EXIT_CODE
}

function action_set_hotel_width () {
    echo; info_msg "Type hotel width (${YELLOW}number of rooms per floor${RESET})"\
        "or (${MAGENTA}.back${RESET})."
    while :
    do
        ROOM_COUNT=`fetch_data_from_user 'RoomCount'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $ROOM_COUNT
        if [ $? -ne 0 ]; then
            warning_msg "Room count must be a number, not (${RED}$ROOM_COUNT${RESET})."
            echo; continue
        fi; break
    done
    set_hotel_width "$ROOM_COUNT"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set hotel width (${RED}$ROOM_COUNT${RESET})."
    else
        ok_msg "Successfully set hotel width (${GREEN}$ROOM_COUNT${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_hotel_height () {
    echo; info_msg "Type hotel height (${YELLOW}number of floors${RESET})"\
        "or (${MAGENTA}.back${RESET})."
    while :
    do
        FLOOR_COUNT=`fetch_data_from_user 'FloorCount'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $FLOOR_COUNT
        if [ $? -ne 0 ]; then
            warning_msg "Floor count must be a number, not (${RED}$FLOOR_COUNT${RESET})."
            echo; continue
        fi; break
    done
    set_hotel_height "$FLOOR_COUNT"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set hotel height (${RED}$FLOOR_COUNT${RESET})."
    else
        ok_msg "Successfully set hotel heigth (${GREEN}$FLOOR_COUNT${RESET})."
    fi
    return $EXIT_CODE
}

function action_plaza_hotel_self_destruct () {
    echo; info_msg "You are about to delete all (${RED}$SCRIPT_NAME${RESET})"\
        "project files from directory (${RED}$MD_DEFAULT['project-path']${RESET})."
    fetch_ultimatum_from_user "${YELLOW}Are you sure about this? Y/N${RESET}"
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    check_safety_on
    if [ $? -ne 0 ]; then
        echo; warning_msg "Safety is (${GREEN}ON${RESET})! Aborting self destruct sequence."
        return 0
    fi; echo
    symbol_msg "${RED}$SCRIPT_NAME${RESET}" "Initiating self destruct sequence!"
    action_self_destruct
    local EXIT_CODE=$?
    if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "(${RED}$SCRIPT_NAME${RESET}) self destruct sequence failed!"
    else
        ok_msg "Destruction complete!"\
            "Project (${GREEN}$SCRIPT_NAME${RESET}) removed from system."
    fi
    return $EXIT_CODE
}

function action_set_client_guest_list () {
    echo; info_msg "Type guest list as aliases separated by commas or (${MAGENTA}.back${RESET})."
    symbol_msg "${BLUE}EXAMPLE${RESET}" "UnitLost1,UnitLost2,UnitLost3,..."
    GUEST_LIST=`fetch_data_from_user 'GuestList'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    set_guest_list "$GUEST_LIST"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set client guest list (${RED}$GUEST_LIST${RESET})."
    else
        ok_msg "Successfully set client guest list (${GREEN}$GUEST_LIST${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_guest_of_client_alias () {
    echo; info_msg "Type alias of the client expecting you or (${MAGENTA}.back${RESET})."
    GUEST_OF=`fetch_data_from_user 'GuestOf'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    set_guest_of_alias "$GUEST_OF"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set guest of client alias (${RED}$GUEST_OF${RESET})."
    else
        ok_msg "Successfully set guest of client alias (${GREEN}$GUEST_OF${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_target_hotel_room_number () {
    echo; info_msg "Type target hotel room number or (${MAGENTA}.back${RESET})."
    while :
    do
        ROOM_NUMBER=`fetch_data_from_user 'RoomNumber'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $ROOM_NUMBER
        if [ $? -ne 0 ]; then
            warning_msg "Room number must be a number, not (${RED}$ROOM_NUMBER${RESET})."
            echo; continue
        fi; break
    done
    set_target_room_number "$ROOM_NUMBER"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set target room number (${RED}$ROOM_NUMBER${RESET})."
    else
        ok_msg "Successfully set target room number (${GREEN}$ROOM_NUMBER${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_target_hotel_floor_number () {
    echo; info_msg "Type target hotel floor number or (${MAGENTA}.back${RESET})."
    while :
    do
        FLOOR_NUMBER=`fetch_data_from_user 'FloorNumber'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $FLOOR_NUMBER
        if [ $? -ne 0 ]; then
            warning_msg "Floor number must be a number, not (${RED}$FLOOR_NUMBER${RESET})."
            echo; continue
        fi; break
    done
    set_target_floor_number "$FLOOR_NUMBER"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set target floor number (${RED}$FLOOR_NUMBER${RESET})."
    else
        ok_msg "Successfully set target floor number (${GREEN}$FLOOR_NUMBER${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_hotel_floor_access_key () {
    echo; info_msg "Type target hotel floor access key or (${MAGENTA}.back${RESET})."
    ACCESS_KEY=`fetch_data_from_user 'AccessKey'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    set_floor_access_key "$ACCESS_KEY"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set floor access key (${RED}$ACCESS_KEY${RESET})."
    else
        ok_msg "Successfully set floor access key (${GREEN}$ACCESS_KEY${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_client_system_user_name () {
    echo; info_msg "Type client system user name or (${MAGENTA}.back${RESET})."
    USERNAME=`fetch_data_from_user 'UserName'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    set_client_system_user_name "$USERNAME"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set client system user name (${RED}$USERNAME${RESET})."
    else
        ok_msg "Successfully set client system user name (${GREEN}$USERNAME${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_room_capacity () {
    echo; info_msg "Type number of orbitals per room or (${MAGENTA}.back${RESET})."
    while :
    do
        CAPACITY=`fetch_data_from_user 'RoomCapacity'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $CAPACITY
        if [ $? -ne 0 ]; then
            warning_msg "Room capacity must be a number, not (${RED}$CAPACITY${RESET})."
            echo; continue
        fi; break
    done
    set_room_capacity "$CAPACITY"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${BLUE}$SCRIPT_NAME${RESET})"\
            "room capacity (${RED}$CAPACITY${RESET})."
    else
        ok_msg "Successfully set room capacity (${GREEN}$CAPACITY${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_chatroom_buffer_size_in_bytes () {
    echo; info_msg "Type room buffer size in bytes or (${MAGENTA}.back${RESET})."
    while :
    do
        BUFFER_SIZE=`fetch_data_from_user 'BufferSize'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $BUFFER_SIZE
        if [ $? -ne 0 ]; then
            warning_msg "Room buffer size must be a number, not (${RED}$BUFFER_SIZE${RESET})."
            echo; continue
        fi; break
    done
    set_room_buffer_size "$BUFFER_SIZE"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${BLUE}$SCRIPT_NAME${RESET})"\
            "room buffer size (${RED}$BUFFER_SIZE${RESET})."
    else
        ok_msg "Successfully set room buffer size (${GREEN}$BUFFER_SIZE${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_chatroom_port_number () {
    echo; info_msg "Type room port number or (${MAGENTA}.back${RESET})."
    while :
    do
        PORT_NUMBER=`fetch_data_from_user 'PortNumber'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_value_is_number $PORT_NUMBER
        if [ $? -ne 0 ]; then
            warning_msg "Room port must be a number, not (${RED}$PORT_NUMBER${RESET})."
            echo; continue
        fi; break
    done
    set_room_port_number "$PORT_NUMBER"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${BLUE}$SCRIPT_NAME${RESET})"\
            "room port number (${RED}$PORT_NUMBER${RESET})."
    else
        ok_msg "Successfully set room port number (${GREEN}$PORT_NUMBER${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_server_address () {
    echo; info_msg "Type (${BLUE}$SCRIPT_NAME${RESET}) server IPv4 address"\
        "or (${MAGENTA}.back${RESET})."
    while :
    do
        ADDRESS=`fetch_data_from_user 'IPv4Address'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_is_ipv4_address "$ADDRESS"
        if [ $? -ne 0 ]; then
            warning_msg "Server address must be IPv4, not (${RED}$ADDRESS${RESET})."
            echo; continue
        fi; break
    done
    set_server_address "$ADDRESS"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${BLUE}$SCRIPT_NAME${RESET})"\
            "room port number (${RED}$ADDRESS${RESET})."
    else
        ok_msg "Successfully set (${BLUE}$SCRIPT_NAME${RESET})"\
            "server address (${GREEN}$ADDRESS${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_client_alias () {
    echo; info_msg "Type your alias or (${MAGENTA}.back${RESET})."
    ALIAS=`fetch_data_from_user 'Alias'`
    if [ $? -ne 0 ]; then
        echo; info_msg "Aborting action."
        return 0
    fi
    set_alias "$ALIAS"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set your alias (${RED}$ALIAS${RESET})."
    else
        ok_msg "Successfully set your alias (${GREEN}$ALIAS${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_server_state_file_path () {
    echo; info_msg "Type absolute file path or (${MAGENTA}.back${RESET})."
    while :
    do
        FILE_PATH=`fetch_data_from_user 'FilePath'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_file_exists "$FILE_PATH"
        if [ $? -ne 0 ]; then
            warning_msg "File (${RED}$FILE_PATH${RESET}) does not exists."
            echo
        fi; break
    done
    set_server_state_file "$FILE_PATH"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$FILE_PATH${RESET}) as"\
            "(${BLUE}$SCRIPT_NAME${RESET}) server state file."
    else
        ok_msg "Successfully set server state file (${GREEN}$FILE_PATH${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_server_state_fifo_path () {
    echo; info_msg "Type absolute fifo pipe path or (${MAGENTA}.back${RESET})."
    while :
    do
        FIFO_PATH=`fetch_data_from_user 'FifoPath'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_fifo_exists "$FIFO_PATH"
        if [ $? -ne 0 ]; then
            warning_msg "File (${RED}$FILE_PATH${RESET}) does not exists."
            echo; continue
        fi; break
    done
    set_server_state_fifo "$FIFO_PATH"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$FIFO_PATH${RESET}) as"\
            "(${BLUE}$SCRIPT_NAME${RESET}) server state fifo."
    else
        ok_msg "Successfully set server state fifo pipe (${GREEN}$FIFO_PATH${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_server_response_fifo_path () {
    echo; info_msg "Type absolute fifo pipe path or (${MAGENTA}.back${RESET})."
    while :
    do
        FIFO_PATH=`fetch_data_from_user 'FifoPath'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_fifo_exists "$FIFO_PATH"
        if [ $? -ne 0 ]; then
            warning_msg "File (${RED}$FILE_PATH${RESET}) does not exists."
            echo; continue
        fi; break
    done
    set_server_response_fifo "$FIFO_PATH"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$FIFO_PATH${RESET}) as"\
            "(${BLUE}$SCRIPT_NAME${RESET}) server response fifo."
    else
        ok_msg "Successfully set server response fifo pipe (${GREEN}$FIFO_PATH${RESET})."
    fi
    return $EXIT_CODE
}

function action_set_floor_access_key_file_path () {
    echo; info_msg "Type absolute file path or (${MAGENTA}.back${RESET})."
    while :
    do
        FILE_PATH=`fetch_data_from_user 'FilePath'`
        if [ $? -ne 0 ]; then
            echo; info_msg "Aborting action."
            return 0
        fi
        check_file_exists "$FILE_PATH"
        if [ $? -ne 0 ]; then
            warning_msg "File (${RED}$FILE_PATH${RESET}) does not exists."
            echo
        fi; break
    done
    set_floor_access_key_file "$FILE_PATH"
    EXIT_CODE=$?
    echo; if [ $EXIT_CODE -ne 0 ]; then
        nok_msg "Something went wrong."\
            "Could not set (${RED}$FILE_PATH${RESET}) as"\
            "(${BLUE}$SCRIPT_NAME${RESET}) floor acces key file."
    else
        ok_msg "Successfully set floor acces key file (${GREEN}$FILE_PATH${RESET})."
    fi
    return $EXIT_CODE
}

# CODE DUMP
