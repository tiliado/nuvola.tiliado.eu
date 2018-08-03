#!/usr/bin/env sh
set -eu
WD="$PWD"
PID=0

finish() {
    if test ${PID}; then kill ${PID}; PID=0; fi
}
trap finish EXIT INT

while true
do
    cd "$WD"
    python3.6 -m nuvola_index -f 'http://127.0.0.1:8001/'
    cd build
    python3 -m http.server 8001 --bind 127.0.0.1 &
    PID=$!
    inotifywait -e modify -e move -e create -e delete -e close_write -e attrib -r "$WD" "$WD/fxwebgen/"
    kill ${PID}
    PID=0
done
