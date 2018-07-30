#!/usr/bin/env sh
set -eu
WD="$PWD"
while true
do
    cd "$WD"
    python3.6 -m nuvola_index -f 'http://127.0.0.1:8000/'
    cd build
    python3 -m http.server &
    PID=$!
    inotifywait -e modify -e move -e create -e delete -e close_write -e attrib -r "$WD"
    kill ${PID}
done
