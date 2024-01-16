#!/usr/bin/env sh

if [ -z "$2" ]; then
	MAIN=project4
else
	MAIN=$1
	shift
fi

ARG="$1"
shift

pyb $MAIN -P inputfile="$ARG" "$@" 2>&1
