#!/bin/sh

if [ -z "$1" ]; then
    echo "Use: $0 target-directory" >&2
    exit 1
fi

TARGET="$1"

mkdir -p "${TARGET}"
git archive master | tar -x -C "${TARGET}"

find "${TARGET}" | while read filename; do
	echo $filename
done

