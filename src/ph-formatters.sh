#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# FORMATTERS

function format_plaza_hotel_client_explore_arguments () {
    local ARGUMENTS=(
        "--script-name=${SCRIPT_NAME}"
        "--running-mode=client"
        "--client-type=guest"
        "--operation=join"
        "--silent-flag=${MD_DEFAULT['silent']}"
        "--state-file=${MD_DEFAULT['state-file']}"
        "--state-fifo=${MD_DEFAULT['state-fifo']}"
        "--response-fifo=${MD_DEFAULT['response-fifo']}"
        "--buffer-size=${MD_DEFAULT['buffer-size']}"
        "--floor-number=${MD_DEFAULT['floor-level']}"
        "--room-number=${MD_DEFAULT['room-number']}"
        "--port-number=${MD_DEFAULT['port-number']}"
        "--address=${MD_DEFAULT['address']}"
        "--alias=${MD_DEFAULT['alias']}"
        "--client-alias=${MD_DEFAULT['guest-of']}"
        "--log-file=${MD_DEFAULT['log-file']}"
    )
    echo -n "${ARGUMENTS[@]}"
    return $?
}

function format_server_update_pipe_writter_arguments () {
    local ARGUMENTS=(
        "--message=${MD_DEFAULT['alias']},.update"
        "--silent=on"
        "--fifo-path=${MD_DEFAULT['state-fifo']}"
        "--log-file=${MD_DEFAULT['log-file']}"
    )
    echo -n "${ARGUMENTS[@]}"
    return $?
}

function format_plaza_hotel_guest_join_arguments () {
    local ARGUMENTS=(
        "--script-name=${SCRIPT_NAME}"
        "--running-mode=client"
        "--client-type=guest"
        "--operation=join"
        "--silent-flag=${MD_DEFAULT['silent']}"
        "--state-file=${MD_DEFAULT['state-file']}"
        "--state-fifo=${MD_DEFAULT['state-fifo']}"
        "--response-fifo=${MD_DEFAULT['response-fifo']}"
        "--buffer-size=${MD_DEFAULT['buffer-size']}"
        "--floor-number=${MD_DEFAULT['floor-level']}"
        "--room-number=${MD_DEFAULT['room-number']}"
        "--port-number=${MD_DEFAULT['port-number']}"
        "--address=${MD_DEFAULT['address']}"
        "--alias=${MD_DEFAULT['alias']}"
        "--client-alias=${MD_DEFAULT['guest-of']}"
        "--log-file=${MD_DEFAULT['log-file']}"
    )
    echo -n "${ARGUMENTS[@]}"
    return $?
}

function format_plaza_hotel_client_checkin_arguments () {
    local ARGUMENTS=(
        "--script-name=${SCRIPT_NAME}"
        "--running-mode=client"
        "--client-type=client"
        "--operation=check-in"
        "--silent-flag=${MD_DEFAULT['silent']}"
        "--state-file=${MD_DEFAULT['state-file']}"
        "--state-fifo=${MD_DEFAULT['state-fifo']}"
        "--response-fifo=${MD_DEFAULT['response-fifo']}"
        "--buffer-size=${MD_DEFAULT['buffer-size']}"
        "--port-number=${MD_DEFAULT['port-number']}"
        "--address=${MD_DEFAULT['address']}"
        "--floor-number=${MD_DEFAULT['floor-level']}"
        "--room-number=${MD_DEFAULT['room-number']}"
        "--alias=${MD_DEFAULT['alias']}"
        "--access-key=${MD_DEFAULT['access-key']}"
        "--guest-list=${MD_DEFAULT['guest-list']}"
        "--log-file=${MD_DEFAULT['log-file']}"
    )
    echo -n "${ARGUMENTS[@]}"
    return $?
}

function format_plaza_hotel_server_arguments () {
    ARGUMENTS=()
    for opt_arg in $@; do
        case "$opt_arg" in
            --key-file=*)
                local ARGUMENT=(
                    ${ARGUMENTS[@]} "--key-file=${opt_arg#*=}"
                )
                ;;
            --state-file=*)
                local ARGUMENT=(
                    ${ARGUMENTS[@]} "--state-file=${opt_arg#*=}"
                )
                ;;
            --static-floor-keys=*)
                local ARGUMENT=(
                    ${ARGUMENTS[@]} "--static-floor-keys=${opt_arg#*=}"
                )
                ;;
        esac
    done
    if [ ${#ARGUMENTS[@]} -eq 0 ]; then
        local ARGUMENT=( "--state-file=${MD_DEFAULT['state-file']}" )
    fi
    local ARGUMENTS=(
        ${ARGUMENTS[@]}
        "--script-name=${SCRIPT_NAME}"
        "--running-mode=server"
        "--silent-flag=${MD_DEFAULT['silent']}"
        "--state-fifo=${MD_DEFAULT['state-fifo']}"
        "--response-fifo=${MD_DEFAULT['response-fifo']}"
        "--buffer-size=${MD_DEFAULT['buffer-size']}"
        "--port-number=${MD_DEFAULT['port-number']}"
        "--address=${MD_DEFAULT['address']}"
        "--hotel-height=${MD_DEFAULT['floor-count']}"
        "--hotel-width=${MD_DEFAULT['room-count']}"
        "--room-capacity=${MD_DEFAULT['room-capacity']}"
        "--log-file=${MD_DEFAULT['log-file']}"
        "--file-permissions=${MD_DEFAULT['file-permissions']}"
    )
    echo -n "${ARGUMENTS[@]}"
    return $?
}
