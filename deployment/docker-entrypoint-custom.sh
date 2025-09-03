#!/bin/bash

# Custom entrypoint script for NetBox with plugin migration support

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
timeout=30
counter=0

while ! python3 /opt/netbox/netbox/manage.py showmigrations >/dev/null 2>&1; do
    if [ $counter -ge $timeout ]; then
        echo "❌ Database connection timeout after ${timeout}s"
        exit 1
    fi
    echo "⏳ Waiting for DB... (${counter}s / ${timeout}s)"
    sleep 3
    counter=$((counter + 3))
done

echo "✅ Database is ready"

# Run migrations
echo "🔄 Running database migrations..."
cd /opt/netbox/netbox

# Run core NetBox migrations first
python3 manage.py migrate --run-syncdb

# Check if plugin tables exist, if not create them
echo "🔧 Ensuring plugin tables exist..."

# Create the plugin tables using SQL if they don't exist
python3 -c "
import os
import sys
import django
from django.conf import settings

# Add NetBox to path
sys.path.insert(0, '/opt/netbox/netbox')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'netbox.settings')
django.setup()

from django.db import connection
from django.core.management.sql import sql_create_index
from django.apps import apps

# Get our plugin models
try:
    app_config = apps.get_app_config('netbox_scion')
    models = app_config.get_models()
    
    with connection.cursor() as cursor:
        # Create tables for each model
        for model in models:
            table_name = model._meta.db_table
            
            # Check if table exists
            cursor.execute(\"\"\"
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_name = %s
            \"\"\", [table_name])
            
            if cursor.fetchone()[0] == 0:
                print(f'Creating table {table_name}...')
                
                # Create the SQL for the table
                from django.db import connection
                from django.core.management.sql import sql_create_index
                from django.db.backends.utils import names_digest
                
                sql_statements = connection.ops.sql_create_model(model, [], [])
                for statement in sql_statements:
                    cursor.execute(statement)
                
                print(f'✅ Created table {table_name}')
            else:
                print(f'✅ Table {table_name} already exists')
                
except Exception as e:
    print(f'⚠️  Plugin table creation warning: {e}')
    pass
"

# Run any remaining migrations
echo "🔄 Running final migrations..."
python3 manage.py migrate

# Collect static files
echo "📦 Collecting static files..."
python3 manage.py collectstatic --no-input

echo "🚀 Starting NetBox..."

# Execute the original command
exec "$@"
