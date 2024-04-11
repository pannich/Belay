#!/bin/bash

DATABASE=../migration/belay.db
MIGRATION_DIR=../migration

for MIGRATION_FILE in $MIGRATION_DIR/*.sql; do
    echo "Applying migration: $MIGRATION_FILE"
    sqlite3 $DATABASE < $MIGRATION_FILE
done
