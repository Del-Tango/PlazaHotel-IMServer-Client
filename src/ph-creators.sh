#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# CREATORS

function create_plaza_hotel_menu_controllers () {
    create_main_menu_controller
    create_plaza_hotel_menu_controller
    create_im_client_menu_controller
    create_im_client_restricted_menu_controller
    create_log_viewer_menu_cotroller
    create_settings_menu_controller
    done_msg "${BLUE}$SCRIPT_NAME${RESET} controller construction complete."
    return 0
}

function create_im_client_menu_controller () {
    create_menu_controller "$IM_CLIENT_CONTROLLER_LABEL" \
        "${CYAN}$IM_CLIENT_CONTROLLER_DESCRIPTION${RESET}" \
        "$IM_CLIENT_CONTROLLER_OPTIONS"
    return $?
}

function create_im_client_restricted_menu_controller () {
    create_menu_controller "$IM_CLIENT_RESTRICTED_CONTROLLER_LABEL" \
        "${CYAN}$IM_CLIENT_RESTRICTED_CONTROLLER_DESCRIPTION${RESET}" \
        "$IM_CLIENT_RESTRICTED_CONTROLLER_OPTIONS"
    return $?
}

function create_plaza_hotel_menu_controller () {
    create_menu_controller "$PLAZA_HOTEL_CONTROLLER_LABEL" \
        "${CYAN}$PLAZA_HOTEL_CONTROLLER_DESCRIPTION${RESET}" \
        "$PLAZA_HOTEL_CONTROLLER_OPTIONS"
    return $?
}

function create_main_menu_controller () {
    create_menu_controller "$MAIN_CONTROLLER_LABEL" \
        "${CYAN}$MAIN_CONTROLLER_DESCRIPTION${RESET}" "$MAIN_CONTROLLER_OPTIONS"
    return $?
}

function create_log_viewer_menu_cotroller () {
    create_menu_controller "$LOGVIEWER_CONTROLLER_LABEL" \
        "${CYAN}$LOGVIEWER_CONTROLLER_DESCRIPTION${RESET}" \
        "$LOGVIEWER_CONTROLLER_OPTIONS"
    return $?
}

function create_settings_menu_controller () {
    create_menu_controller "$SETTINGS_CONTROLLER_LABEL" \
        "${CYAN}$SETTINGS_CONTROLLER_DESCRIPTION${RESET}" \
        "$SETTINGS_CONTROLLER_OPTIONS"

    info_msg "Setting ${CYAN}$SETTINGS_CONTROLLER_LABEL${RESET} extented"\
        "banner function ${MAGENTA}display_plaza_hotel_settings${RESET}..."
    set_menu_controller_extended_banner "$SETTINGS_CONTROLLER_LABEL" \
        'display_plaza_hotel_settings'

    return 0
}

