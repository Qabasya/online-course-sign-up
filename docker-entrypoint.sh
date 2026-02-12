#!/bin/sh

chown -R 1000:1003 /app/logs /app/db

gosu 1000:1003 "$@"
