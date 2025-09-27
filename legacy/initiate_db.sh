# To manually stop postgres server:
# pg_ctl -D ./pgdata stop -m fast


#!/usr/bin/env bash
set -euo pipefail

# Defaults
PGDATA="./pgdata"
PGPORT=5433
DBNAME="spotify_db"

# Ensure pgdata exists
if [ ! -d "$PGDATA" ]; then
  echo "Initializing database cluster..."
  initdb -D "$PGDATA"
fi

# Start postgres
echo "Starting postgres..."
pg_ctl -D "$PGDATA" -o "-p $PGPORT" -l logfile start

# Wait until server is ready
until pg_isready -p $PGPORT > /dev/null 2>&1; do
  echo "Waiting for postgres to start..."
  sleep 1
done

# Create user and db if not exist
psql -p $PGPORT -U $USER -d postgres -tc "SELECT 1 FROM pg_roles WHERE rolname='$USER'" | grep -q 1 || \
  psql -p $PGPORT -U $USER -d postgres -c "CREATE USER $USER WITH PASSWORD 'password';"

psql -p $PGPORT -U $USER -d postgres -tc "SELECT 1 FROM pg_database WHERE datname='$DBNAME'" | grep -q 1 || \
  psql -p $PGPORT -U $USER -d postgres -c "CREATE DATABASE $DBNAME OWNER $USER;"

# Run DDL
psql -p $PGPORT -U $USER -d $DBNAME -f ddl.sql

# Load CSVs
for f in data/*.csv; do
  if [ -f "$f" ]; then
    echo "Loading $f..."
    psql -p $PGPORT -U $USER -d $DBNAME -c "\COPY track FROM '$f' CSV HEADER;"
  fi
done

echo "All done! Connect with: psql -p $PGPORT -U $USER -d $DBNAME"