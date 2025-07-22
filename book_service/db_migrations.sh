#!/bin/sh

flask db init
flask db upgrade

echo "Flask migrations completed."

exec "$@"
