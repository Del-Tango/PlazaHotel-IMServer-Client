#!/bin/bash
#
# Regards, the Alveare Solutions society.
#
# GENERAL

function send_plaza_hotel_state_file_update_signal () {
    ARGUMENTS=( `format_server_update_pipe_writter_arguments` )
    ${PH_CARGO['pipe-writter']} ${ARGUMENTS[@]}
    return $?
}

function trap_plaza_hotel_client () {
    trap "echo Konversation Terminated!; sleep 1; exit 1" 1 2 3 15 20
    return $?
}
