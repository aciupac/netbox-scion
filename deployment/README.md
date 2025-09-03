# NetBox SCION Plugin - Deployment

A comprehensive NetBox plugin for managing SCION (Scalability, Control, and Isolation On Next-generation networks) infrastructure.

## 🚀 Quick Installation

### Prerequisites
- Docker and Docker Compose
- Existing NetBox deployment using netbox-docker

### Method 1: Pip Package Installation (Recommended)

This method installs the plugin directly from PyPI, making updates easier.

#### Step 1: Copy Files
```bash
# Copy the deployment files to your netbox-docker directory
cp -r deployment/* /path/to/your/netbox-docker/

# Or copy individual files:
cp Dockerfile.netbox-pip /path/to/your/netbox-docker/  # For PyPI installation
cp docker-entrypoint-custom.sh /path/to/your/netbox-docker/
cp plugin_requirements.txt /path/to/your/netbox-docker/
```

#### Step 2: Update Docker Compose
Update your existing `docker-compose.yml` to use the custom Dockerfile:

```yaml
services:
  netbox: &netbox
    build:
      context: .
      dockerfile: Dockerfile.netbox-pip  # For PyPI installation
    # Remove the 'image:' line if present
    # ... rest of your existing configuration
```

#### Step 3: Update Configuration
Add to your NetBox `plugins.py` file (or `configuration/plugins.py` if using structured configuration):

```python
PLUGINS = [
    'netbox_scion',
    # Your existing plugins...
]
```

Add to your `env/netbox.env`:
```bash
PLUGINS_REQUIREMENTS=netbox-scion==1.0.0
# Or if you have existing plugins:
# PLUGINS_REQUIREMENTS=existing_plugin1,existing_plugin2,netbox-scion==1.0.0
```

#### Step 4: Deploy
```bash
cd /path/to/your/netbox-docker

# Standard deployment (preserves existing data):
docker-compose down
docker-compose build --no-cache netbox
docker-compose up -d

# For fresh installation only (removes all NetBox data):
# WARNING: This will delete ALL NetBox data including users and configurations
# docker-compose down
# docker volume rm netbox-docker_netbox-postgres-data
# docker-compose build --no-cache netbox  
# docker-compose up -d
# docker exec -it netbox-docker-netbox-1 /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py createsuperuser
```

#### Step 5: Update Plugin (when needed)
To update the plugin to a newer version:

```bash
# Update the version in plugin_requirements.txt
echo "netbox-scion==1.1.0" > plugin_requirements.txt

# Rebuild and restart
docker-compose down
docker-compose build --no-cache netbox
docker-compose up -d

# Check for any pending migrations
docker exec netbox-container /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py showmigrations netbox_scion
```

### Method 2: Local Wheel Installation

If you prefer to use the local wheel file instead of PyPI:

```bash
# Copy files including local wheel
cp Dockerfile.netbox-local /path/to/your/netbox-docker/
cp plugins/netbox_scion-1.0.0-py3-none-any.whl /path/to/your/netbox-docker/plugins/

# Update docker-compose.yml to use:
# dockerfile: Dockerfile.netbox-local
```

### Method 3: Manual Installation

If you prefer not to use a custom Docker image:

```bash
# Copy wheel to your running NetBox container (if using local wheel)
docker cp plugins/netbox_scion-1.0.0-py3-none-any.whl netbox-container:/tmp/

# Install the plugin (choose one method):
# Method A: From PyPI (recommended)
docker exec netbox-container /opt/netbox/venv/bin/pip install netbox-scion==1.0.0

# Method B: From local wheel
docker exec netbox-container /opt/netbox/venv/bin/pip install /tmp/netbox_scion-1.0.0-py3-none-any.whl

# Run migrations
docker exec netbox-container /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py migrate

# Restart NetBox
docker-compose restart netbox
```

## ✅ Verification

1. **Check Plugin Installation:**
```bash
docker exec netbox-container /opt/netbox/venv/bin/pip list | grep netbox-scion
```

2. **Access NetBox Web Interface:**
   - Navigate to your NetBox URL
   - Look for "SCION" menu in the sidebar
   - You should see: Organizations, ISD-ASes, SCION Link Assignments

3. **API Access:**
   - Organizations: `/api/plugins/scion/organizations/`
   - ISD-ASes: `/api/plugins/scion/isd-ases/`
   - Link Assignments: `/api/plugins/scion/link-assignments/`

## 🏗️ Features

- **Organizations**: Manage SCION organizations with short/full names
- **ISD-ASes**: ISD-AS management with regex validation and core node support
- **SCION Link Assignments**: Interface assignments with customer management and Zendesk integration
- **Full REST API**: Complete CRUD operations
- **Export Support**: CSV/Excel export capabilities
- **Advanced Filtering**: Customer-based filtering for link assignments
- **Audit Logging**: Built-in change tracking

## 🔧 Files Included

## 📁 Deployment Files

- `Dockerfile.netbox-fixed` - Custom NetBox Dockerfile with plugin installation
- `docker-entrypoint-custom.sh` - Enhanced entrypoint with auto-migration
- `plugin_requirements.txt` - Plugin requirements for pip installation
- `plugins/netbox_scion-1.0.0-py3-none-any.whl` - Plugin wheel package (alternative to PyPI)
- `docker-compose.yml` - Example Docker Compose configuration
- `configuration.py.example` - Example NetBox configuration
- `netbox.env.example` - Example environment variables

## 🐛 Troubleshooting

### Plugin Not Appearing
1. Check plugin is installed: `docker exec netbox-container /opt/netbox/venv/bin/pip list | grep netbox-scion`
2. Check configuration: Ensure `netbox_scion` is in `PLUGINS` list
3. Check environment: Ensure `PLUGINS_REQUIREMENTS=netbox_scion` in netbox.env
4. Restart NetBox: `docker-compose restart netbox`

### Database Errors
1. The custom entrypoint automatically handles migrations
2. For manual setup: `docker exec netbox-container /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py migrate`

**Custom Field Data Error Fix:**
If you encounter "null value in column 'custom_field_data'" errors:
1. This has been fixed in the latest wheel package (includes migration 0002)
2. The migration will automatically add the required custom_field_data columns
3. Restart NetBox after installation to apply the migration

### Menu Issues
- Plugin appears under "Plugins" > "SCION" section in NetBox sidebar
- This is standard behavior for NetBox 4.3+ plugin system
- Look for "Plugins" → "SCION" in the navigation menu
- Individual menu items: Organizations, ISD-ASes, SCION Link Assignments

**Menu Collapsing Issue:**
If the sidebar menu collapses when you lose focus, this is typically due to:
1. Browser viewport size - NetBox auto-collapses on smaller screens
2. NetBox theme settings - check User Preferences → UI Theme
3. JavaScript conflicts - try refreshing the page or clearing cache

## 📊 Plugin Structure

```
Plugins > SCION Menu:
├── Organizations
│   ├── List/Add/Edit/Delete
│   └── Export to CSV/Excel
├── ISD-ASes  
│   ├── List/Add/Edit/Delete
│   ├── Core nodes management
│   └── Organization association
└── SCION Link Assignments
    ├── List/Add/Edit/Delete
    ├── Customer management
    ├── Zendesk ticket integration
    └── Advanced filtering
```

## 🔗 API Examples

Create an organization:
```bash
curl -X POST http://your-netbox/api/plugins/scion/organizations/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"short_name": "ACME", "full_name": "ACME Corporation"}'
```

Create an ISD-AS:
```bash
curl -X POST http://your-netbox/api/plugins/scion/isd-ases/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"isd_as": "1-ff00:0:110", "organization": 1, "cores": ["core1.example.com"]}'
```

## 📝 License

Apache License 2.0
docker exec netbox /opt/netbox/venv/bin/python -m ensurepip --upgrade
docker exec netbox /opt/netbox/venv/bin/pip install netbox-scion==1.0.0

# Add to configuration.py:
# PLUGINS = ['netbox_scion']

# Run migrations
docker exec netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py migrate

# Restart NetBox
docker restart netbox
```

## Requirements

- NetBox 3.5+
- Docker with NetBox container
- PostgreSQL database (recommended, but works with other databases)

## Configuration

Add this to your NetBox `configuration.py`:

```python
PLUGINS = [
    'netbox_scion',
]
```

## Verification

After installation:
1. Check the main NetBox navigation for "SCION" menu
2. Visit `/api/plugins/scion/` for API access
3. Access Organizations, ISD-ASes, and Link Assignments

## Troubleshooting

### Pip not found in container
```bash
# Install pip in the virtual environment
docker exec netbox /opt/netbox/venv/bin/python -m ensurepip --upgrade

# Verify pip is working
docker exec netbox /opt/netbox/venv/bin/pip --version
```

### Plugin not appearing after installation
```bash
# Check if plugin is installed
docker exec netbox /opt/netbox/venv/bin/python -c "import netbox_scion; print('Plugin installed successfully')"

# Check NetBox configuration
docker exec netbox grep -n "PLUGINS" /etc/netbox/configuration.py

# Verify migrations ran
docker exec netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py showmigrations netbox_scion
```

### Alternative installation methods
```bash
# Method 1: Direct Python installation
docker exec netbox /opt/netbox/venv/bin/python -c "
import subprocess, sys
subprocess.run([sys.executable, '-m', 'pip', 'install', 'netbox-scion==1.0.0'], check=True)
"

# Method 2: Using setuptools directly
docker exec netbox /opt/netbox/venv/bin/python -c "
import subprocess, sys, os
os.chdir('/tmp')
subprocess.run([sys.executable, 'setup.py', 'install'], check=True)
"
```

## Support

- GitHub: https://github.com/aciupac/netbox-scion
- Documentation: See DOCKER_DEPLOYMENT.md for detailed instructions
