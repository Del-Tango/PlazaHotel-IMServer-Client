#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# LOADERS

function load_plaza_hotel_config () {
    load_plaza_hotel_script_name
    load_plaza_hotel_prompt_string
    load_plaza_hotel_safety
    load_settings_plaza_hotel_default
    load_plaza_hotel_logging_levels
    load_plaza_hotel_cargo
    load_plaza_hotel_dependencies
}

function load_plaza_hotel_dependencies () {
    load_apt_dependencies ${PH_APT_DEPENDENCIES[@]}
    load_pip3_dependencies ${PH_PIP3_DEPENDENCIES[@]}
    return $?
}

function load_plaza_hotel_safety () {
    load_safety $PH_SAFETY
    return $?
}

function load_plaza_hotel_prompt_string () {
    load_prompt_string "$PH_PS3"
    return $?
}

function load_plaza_hotel_logging_levels () {
    load_logging_levels ${PH_LOGGING_LEVELS[@]}
    return $?
}

function load_plaza_hotel_cargo () {
    for plaza_hotel_cargo in ${!PH_CARGO[@]}; do
        load_cargo \
            "$plaza_hotel_cargo" ${PH_CARGO[$plaza_hotel_cargo]}
    done
    return $?
}

function load_settings_plaza_hotel_default () {
    for plaza_hotel_setting in ${!PH_DEFAULT[@]}; do
        load_default_setting \
            "$plaza_hotel_setting" ${PH_DEFAULT[$plaza_hotel_setting]}
    done
    return $?
}

function load_settings_plaza_hotel_import () {
    for plaza_hotel_import in ${!PH_IMPORTS[@]}; do
        plaza_hotel_import \
            "$plaza_hotel_import" ${PH_IMPORTS[$plaza_hotel_import]}
    done
    return $?
}

function load_plaza_hotel_script_name () {
    load_script_name "$PH_SCRIPT_NAME"
    return $?
}

# SETUP

function plaza_hotel_project_setup () {
    lock_and_load
    load_plaza_hotel_config
    create_plaza_hotel_menu_controllers
    setup_plaza_hotel_menu_controllers
}

function setup_plaza_hotel_menu_controllers () {
    setup_plaza_hotel_dependencies
    setup_main_menu_controller
    setup_log_viewer_menu_controller
    setup_plaza_hotel_menu_controller
    setup_im_client_menu_controller
    setup_im_client_restricted_menu_controller
    setup_settings_menu_controller
    done_msg "${BLUE}$SCRIPT_NAME${RESET} controller setup complete."
    return 0
}

# SETUP DEPENDENCIES

function setup_plaza_hotel_dependencies () {
    apt_install_dependencies
    pip3_install_dependencies
    return $?
}

# IM CLIENT RESTRICTED MENU SETUP

function setup_im_client_restricted_menu_controller() {
    setup_im_client_restricted_menu_option_book_room
    setup_im_client_restricted_menu_option_join_room
    setup_im_client_restricted_menu_option_explore_room
    setup_im_client_restricted_menu_option_back
    done_msg "(${CYAN}$IM_CLIENT_RESTRICTED_CONTROLLER_LABEL${RESET}) controller"\
        "option binding complete."
    return 0
}

function setup_im_client_restricted_menu_option_book_room () {
    setup_menu_controller_action_option \
        "$IM_CLIENT_RESTRICTED_CONTROLLER_LABEL" "I-Need-A-Room" \
        'action_plaza_hotel_interactive_client_book_room'
    return $?
}

function setup_im_client_restricted_menu_option_join_room () {
    setup_menu_controller_action_option \
        "$IM_CLIENT_RESTRICTED_CONTROLLER_LABEL" "They-Are-Expecting-Me" \
        'action_plaza_hotel_interactive_guest_join_room'
    return $?
}

function setup_im_client_restricted_menu_option_explore_room () {
    setup_menu_controller_action_option \
        "$IM_CLIENT_RESTRICTED_CONTROLLER_LABEL" "I-Want-To-Network" \
        'action_plaza_hotel_interactive_client_explore_room'
    return $?
}

function setup_im_client_restricted_menu_option_back () {
    setup_menu_controller_action_option \
        "$IM_CLIENT_RESTRICTED_CONTROLLER_LABEL" "Back" 'action_back'
    return $?
}

# IM CLIENT MENU SETUP

function setup_im_client_menu_controller() {
    setup_im_client_menu_option_book_room
    setup_im_client_menu_option_join_room
    setup_im_client_menu_option_explore_room
    setup_im_client_menu_option_back
    done_msg "(${CYAN}$IM_CLIENT_CONTROLLER_LABEL${RESET}) controller"\
        "option binding complete."
    return 0
}

function setup_im_client_menu_option_book_room () {
    setup_menu_controller_action_option \
        "$IM_CLIENT_CONTROLLER_LABEL" "Book-Room" \
        'action_plaza_hotel_client_book_room'
    return $?
}

function setup_im_client_menu_option_join_room () {
    setup_menu_controller_action_option \
        "$IM_CLIENT_CONTROLLER_LABEL" "Join-Room" \
        'action_plaza_hotel_guest_join_room'
    return $?
}

function setup_im_client_menu_option_explore_room () {
    setup_menu_controller_action_option \
        "$IM_CLIENT_CONTROLLER_LABEL" "Explore-Room" \
        'action_plaza_hotel_client_explore_room'
    return $?
}

function setup_im_client_menu_option_back () {
    setup_menu_controller_action_option \
        "$IM_CLIENT_CONTROLLER_LABEL" "Back" \
        'action_back'
    return $?
}

# PLAZA HOTEL MENU SETUP

function setup_plaza_hotel_menu_controller () {
    setup_plaza_hotel_menu_option_start_plaza_server
    setup_plaza_hotel_menu_option_start_plaza_client
#   setup_plaza_hotel_menu_option_start_plaza_bot
    setup_plaza_hotel_menu_option_help
    setup_plaza_hotel_menu_option_back
    done_msg "(${CYAN}$PLAZA_HOTEL_CONTROLLER_LABEL${RESET}) controller"\
        "option binding complete."
    return 0
}

function setup_plaza_hotel_menu_option_start_plaza_server () {
    setup_menu_controller_action_option \
        "$PLAZA_HOTEL_CONTROLLER_LABEL"  "Start-Plaza-Hotel-Server" \
        'action_start_plaza_hotel_server'
    return $?
}

function setup_plaza_hotel_menu_option_start_plaza_client () {
    setup_menu_controller_menu_option \
        "$PLAZA_HOTEL_CONTROLLER_LABEL"  "Start-Plaza-Hotel-Client" \
        "$IM_CLIENT_CONTROLLER_LABEL"
    return $?
}

function setup_plaza_hotel_menu_option_help () {
    setup_menu_controller_action_option \
        "$PLAZA_HOTEL_CONTROLLER_LABEL"  "Help" 'action_help'
    return $?
}

function setup_plaza_hotel_menu_option_back () {
    setup_menu_controller_action_option \
        "$PLAZA_HOTEL_CONTROLLER_LABEL"  "Back" 'action_back'
    return $?
}

# MAIN MENU SETUP

function setup_main_menu_controller () {
    setup_main_menu_option_plaza_hotel
    setup_main_menu_option_log_viewer
    setup_main_menu_option_control_panel
    setup_main_menu_option_self_destruct
    setup_main_menu_option_back
    done_msg "${CYAN}$MAIN_CONTROLLER_LABEL${RESET} controller option"\
        "binding complete."
    return 0
}

function setup_main_menu_option_self_destruct () {
    setup_menu_controller_action_option \
        "$MAIN_CONTROLLER_LABEL"  "Self-Destruct" \
        'action_plaza_hotel_self_destruct'
    return $?
}

function setup_main_menu_option_plaza_hotel () {
    setup_menu_controller_menu_option \
        "$MAIN_CONTROLLER_LABEL"  "Plaza-Hotel" \
        "$PLAZA_HOTEL_CONTROLLER_LABEL"
    return $?
}

function setup_main_menu_option_log_viewer () {
    setup_menu_controller_menu_option \
        "$MAIN_CONTROLLER_LABEL"  "Log-Viewer" \
        "$LOGVIEWER_CONTROLLER_LABEL"
    return $?
}

function setup_main_menu_option_control_panel () {
    setup_menu_controller_menu_option \
        "$MAIN_CONTROLLER_LABEL"  'Control-Panel' \
        "$SETTINGS_CONTROLLER_LABEL"
    return $?
}

function setup_main_menu_option_back () {
    setup_menu_controller_action_option \
        "$MAIN_CONTROLLER_LABEL"  'Back' 'action_back'
    return $?
}

# LOG VIEWER MENU SETUP

function setup_log_viewer_menu_controller () {
    setup_log_viewer_menu_option_display_tail
    setup_log_viewer_menu_option_display_head
    setup_log_viewer_menu_option_display_more
    setup_log_viewer_menu_option_clear_log_file
    setup_log_viewer_menu_option_back
    done_msg "${CYAN}$LOGVIEWER_CONTROLLER_LABEL${RESET} controller option"\
        "binding complete."
    return 0
}

function setup_log_viewer_menu_option_clear_log_file () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Clear-Log' 'action_clear_log_file'
    return $?
}

function setup_log_viewer_menu_option_display_tail () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Display-Tail' 'action_log_view_tail'
    return $?
}

function setup_log_viewer_menu_option_display_head () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Display-Head' 'action_log_view_head'
    return $?
}

function setup_log_viewer_menu_option_display_more () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Display-More' 'action_log_view_more'
    return $?
}

function setup_log_viewer_menu_option_back () {
    setup_menu_controller_action_option \
        "$LOGVIEWER_CONTROLLER_LABEL"  'Back' 'action_back'
    return $?
}

# SETTINGS MENU SETUP

function setup_settings_menu_controller () {
    setup_settings_menu_option_set_safety_on
    setup_settings_menu_option_set_safety_off
    setup_settings_menu_option_set_room_capacity
    setup_settings_menu_option_set_room_buffer_size
    setup_settings_menu_option_set_server_state_file
    setup_settings_menu_option_set_server_state_fifo
    setup_settings_menu_option_set_server_response_fifo
    setup_settings_menu_option_set_floor_key_file
    setup_settings_menu_option_set_room_port_number
    setup_settings_menu_option_set_server_address
    setup_settings_menu_option_set_client_alias
    setup_settings_menu_option_set_client_action
    setup_settings_menu_option_set_client_guest_list
    setup_settings_menu_option_set_guest_of
    setup_settings_menu_option_set_target_room_number
    setup_settings_menu_option_set_target_floor_number
    setup_settings_menu_option_set_floor_access_key
    setup_settings_menu_option_set_client_system_user_details
    setup_settings_menu_option_set_temporary_file
    setup_settings_menu_option_set_log_file
    setup_settings_menu_option_set_log_lines
    setup_settings_menu_option_set_silent_on
    setup_settings_menu_option_set_silent_off
    setup_settings_menu_option_set_hotel_width
    setup_settings_menu_option_set_hotel_height
    setup_settings_menu_option_setup_system_user
    setup_settings_menu_option_purge_system_user
    setup_settings_menu_option_install_dependencies
    setup_settings_menu_option_back
    done_msg "${CYAN}$SETTINGS_CONTROLLER_LABEL${RESET} controller option"\
        "binding complete."
    return 0
}

function setup_settings_menu_option_set_hotel_width () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Hotel-Width' \
        'action_set_hotel_width'
    return $?
}

function setup_settings_menu_option_set_hotel_height () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Hotel-Height' \
        'action_set_hotel_height'
    return $?
}

function setup_settings_menu_option_setup_system_user () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Setup-System-User' \
        'action_setup_system_user'
    return $?
}

function setup_settings_menu_option_purge_system_user () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Purge-System-User' \
        'action_purge_system_user'
    return $?
}

function setup_settings_menu_option_set_safety_on () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Safety-ON' \
        'action_set_safety_on'
    return $?
}

function setup_settings_menu_option_set_safety_off () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Safety-OFF' \
        'action_set_safety_off'
    return $?
}

function setup_settings_menu_option_set_silent_on () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Silent-ON' \
        'action_set_silent_flag_on'
    return $?
}

function setup_settings_menu_option_set_silent_off () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Silent-OFF' \
        'action_set_silent_flag_off'
    return $?
}

function setup_settings_menu_option_set_temporary_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Temporary-File' \
        'action_set_temporary_file'
    return $?
}

function setup_settings_menu_option_set_log_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Log-File' \
        'action_set_log_file'
    return $?
}

function setup_settings_menu_option_set_log_lines () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Log-Lines' \
        'action_set_log_lines'
    return $?
}

function setup_settings_menu_option_install_dependencies () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Install-Dependencies' \
        'action_install_dependencies'
    return $?
}

function setup_settings_menu_option_back () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Back' 'action_back'
    return $?
}

function setup_settings_menu_option_set_room_capacity () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Room-Capacity' \
        'action_set_room_capacity'
    return $?
}

function setup_settings_menu_option_set_room_buffer_size () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Room-Buffer-Size' \
        'action_set_chatroom_buffer_size_in_bytes'
    return $?
}

function setup_settings_menu_option_set_server_state_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-State-File' \
        'action_set_server_state_file_path'
    return $?
}

function setup_settings_menu_option_set_server_state_fifo () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-State-Fifo' \
        'action_set_server_state_fifo_path'
    return $?
}

function setup_settings_menu_option_set_server_response_fifo () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Response-Fifo' \
        'action_set_server_response_fifo_path'
    return $?
}

function setup_settings_menu_option_set_floor_key_file () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Key-File' \
        'action_set_floor_access_key_file_path'
    return $?
}

function setup_settings_menu_option_set_room_port_number () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Port-Number' \
        'action_set_chatroom_port_number'
    return $?
}
function setup_settings_menu_option_set_server_address () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Address' \
        'action_set_server_address'
    return $?
}

function setup_settings_menu_option_set_client_alias () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Client-Alias' \
        'action_set_client_alias'
    return $?
}

function setup_settings_menu_option_set_client_action () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Client-Action' \
        'action_set_client_action'
    return $?
}

function setup_settings_menu_option_set_client_guest_list () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Guest-List' \
        'action_set_client_guest_list'
    return $?
}

function setup_settings_menu_option_set_guest_of () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Guest-Of' \
        'action_set_guest_of_client_alias'
    return $?
}

function setup_settings_menu_option_set_target_room_number () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Hotel-Room' \
        'action_set_target_hotel_room_number'
    return $?
}

function setup_settings_menu_option_set_target_floor_number () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Hotel-Floor' \
        'action_set_target_hotel_floor_number'
    return $?
}

function setup_settings_menu_option_set_floor_access_key () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-Access-Key' \
        'action_set_hotel_floor_access_key'
    return $?
}

function setup_settings_menu_option_set_client_system_user_details () {
    setup_menu_controller_action_option \
        "$SETTINGS_CONTROLLER_LABEL" 'Set-System-User' \
        'action_set_client_system_user_name'
    return $?
}

# CODE DUMP


