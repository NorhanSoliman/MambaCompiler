#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -z "$1" ]; then
	echo "Must specify which project (e.g., project1 or project2 or project3 or project4)"
	exit -1
fi

MAIN=$1

SAVEIFS=$IFS
IFS=$(echo -en "\n\b")
for i in `ls $DIR/examples/$MAIN/*.mb` ; do
	FILE=`basename $i`

	echo "./run.sh $MAIN \"$DIR/examples/$MAIN/$FILE\" 2>&1" >> test.log
	OUTPUT=`./run.sh $MAIN "$DIR/examples/$MAIN/$FILE" 2>&1`
	echo "$OUTPUT" >> test.log

	OUTPUT=`echo "$OUTPUT" | tr '\n' '\r' | sed 's/.*\rCOMPILER OUTPUT START\r------------------------------------------------------------\r//'`
	OUTPUT=`echo "$OUTPUT" | sed 's/------------------------------------------------------------\rCOMPILER OUTPUT END\r.*//' | tr '\r' '\n'`

	if [ "$OUTPUT" == "" ] ; then
		printf '%s' "$OUTPUT" | tr -d '\015' | diff -c "$DIR/expected-output/$MAIN/$FILE.out" - >> test.log
	else
		echo "$OUTPUT" | tr -d '\015' | diff -c "$DIR/expected-output/$MAIN/$FILE.out" - >> test.log
	fi

	if [ $? -eq 0 ] ; then
		echo "Test PASSED: $FILE"
	else
		echo "Test FAILED: $FILE"
	fi
done
IFS=$SAVEIFS
