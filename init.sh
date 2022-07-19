python3 -m venv .venv
source .venv/bin/activate

# setup database if it does not exist with an admin and standard users

DB_FILE="vuln_app.db"

if [ ! -f "$DB_FILE" ]; then
    echo "Initializing database..."
    python ./init_db.py
fi

if [ -f "$DB_FILE" ]; then
    echo "DB file exists: $DB_FILE"
fi