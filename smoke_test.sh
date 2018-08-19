#!/bin/bash

set -e

printf "\ndebug: running integration test..."
./todo.py
printf "\ndebug: adding a todo"
./todo.py --add 'integration test todo'
printf "\ndebug: deleting a todo"
./todo.py --delete 1
