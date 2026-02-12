#!/bin/sh

chown -R 1000:1003 /app/logs /app/db

su-exec 1000:1003 "$@"
