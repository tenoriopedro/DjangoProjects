#!/bin/sh

# The shell will terminate script execution when a command fails
set -e

wait_psql.sh
collectstatic.sh
migrate.sh
runserver.sh