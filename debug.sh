#!/usr/bin/env sh

if [ -z "$2" ]; then
	MAIN=project4
else
	MAIN=$1
	shift
fi

ARG="$1"
shift

PYDEVD_DISABLE_FILE_VALIDATION=1 pyb $MAIN -P inputfile="$ARG" "$@" -P debug=True 2>&1
