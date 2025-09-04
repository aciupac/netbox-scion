# NetBox SCION Plugin - Advanced Deployment Guide

This guide covers advanced installation methods, custom Docker builds, and detailed troubleshooting for the NetBox SCION plugin.

**For simple installation, see the main [README.md](../README.md) first.**

## 🚀 Advanced Installation Methods

### Prerequisites
- Docker and Docker Compose
- Existing NetBox deployment using [netbox-docker](https://github.com/netbox-community/netbox-docker)

### Method 1: Custom Docker Image with PyPI

This method creates a custom Docker image with the plugin pre-installed from PyPI.

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

### Method 2: Custom Docker Image with Local Wheel

If you prefer to use the local wheel file instead of PyPI:

```bash
# Copy files including local wheel
cp Dockerfile.netbox-local /path/to/your/netbox-docker/
cp plugins/netbox_scion-1.0.0-py3-none-any.whl /path/to/your/netbox-docker/plugins/

# Update docker-compose.yml to use:
# dockerfile: Dockerfile.netbox-local
```

### Method 3: Manual Installation in Running Container

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

## 🐛 Detailed Troubleshooting

### Plugin Not Appearing

**For Docker installations:**
```bash
# Check installation
docker exec netbox pip show netbox-scion

# Check logs for errors
docker logs netbox | grep -i error
docker logs netbox | grep -i scion

# Verify plugin loading
docker exec netbox python -c "import netbox_scion; print('Plugin loaded successfully')"

# Restart services
docker-compose restart netbox netbox-worker
```

**For system installations:**
```bash
# Check installation
/opt/netbox/venv/bin/pip show netbox-scion

# Check logs
sudo journalctl -u netbox -f | grep -i scion

# Restart services
sudo systemctl restart netbox netbox-rq
```

### Common Configuration Issues

1. **Plugin in configuration:** Ensure `'netbox_scion'` is in your `PLUGINS` list
2. **Requirements (Docker only):** Check `PLUGINS_REQUIREMENTS=netbox-scion==1.0.0` in `env/netbox.env`
3. **Migrations:** Run `python manage.py migrate` (automatic in Docker)
4. **Permissions:** Ensure NetBox user has proper database permissions
5. **Version mismatch:** Ensure NetBox version compatibility (v4.0+)

### Database Migration Issues

**Automatic migration (Docker):**
The custom entrypoint script automatically handles migrations. If issues persist:

```bash
# Check migration status
docker exec netbox python /opt/netbox/netbox/manage.py showmigrations netbox_scion

# Run migrations manually
docker exec netbox python /opt/netbox/netbox/manage.py migrate netbox_scion
```

**Manual migration (System install):**
```bash
cd /opt/netbox/netbox
python manage.py migrate netbox_scion
```

### Navigation and Menu Issues

**Plugin appears under "SCION" section** in NetBox sidebar, not under "Plugins":
- Look for top-level "SCION" menu
- Individual items: Organizations, ISD-ASes, SCION Link Assignments
- If not visible, check browser cache and try hard refresh (Ctrl+F5)

**Menu Collapsing Issue:**
If the sidebar menu collapses when you lose focus:
1. Browser viewport size - NetBox auto-collapses on smaller screens
2. NetBox theme settings - check User Preferences → UI Theme
3. JavaScript conflicts - try refreshing the page or clearing cache

### Advanced Debugging

**Check Python import:**
```bash
# Docker
docker exec netbox python -c "
import netbox_scion
print(f'Plugin version: {netbox_scion.__version__}')
print(f'Plugin location: {netbox_scion.__file__}')
"

# System
/opt/netbox/venv/bin/python -c "
import netbox_scion
print(f'Plugin version: {netbox_scion.__version__}')
"
```

**Check NetBox configuration:**
```bash
# Docker
docker exec netbox grep -n "PLUGINS" /etc/netbox/configuration.py

# System
grep -n "PLUGINS" /opt/netbox/netbox/netbox/configuration.py
```

**Legacy Installation Cleanup:**
If upgrading from older versions:
```bash
# Remove old installations
pip uninstall netbox-scion
pip install netbox-scion==1.0.0

# Clear Python cache
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +
```

## 📊 Plugin Structure

```
SCION (Top-level menu):
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

---

**For simple installation instructions, see the main [README.md](../README.md).**
