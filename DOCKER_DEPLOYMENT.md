# NetBox SCION Plugin - Docker Deployment Guide

This guide provides multiple methods to deploy the NetBox SCION plugin to your Docker-based NetBox installation.

## Method 1: Using the Wheel Package (Recommended)

### Step 1: Copy the wheel package to your NetBox server
```bash
# Copy the wheel file to your NetBox Docker host
scp dist/netbox_scion-0.1.0-py3-none-any.whl your-server:/path/to/your/netbox/
```

### Step 2: Install the plugin in your NetBox container
```bash
# Option A: If using docker-compose
docker-compose exec netbox /opt/netbox/venv/bin/pip install /opt/netbox/netbox_scion-0.1.0-py3-none-any.whl

# Option B: If using docker run
docker exec -it your-netbox-container /opt/netbox/venv/bin/pip install /path/to/netbox_scion-0.1.0-py3-none-any.whl

# Option C: If pip doesn't exist in venv, install it first
docker exec your-netbox-container /opt/netbox/venv/bin/python -m ensurepip --upgrade
docker exec your-netbox-container /opt/netbox/venv/bin/pip install /path/to/netbox_scion-0.1.0-py3-none-any.whl
```

### Step 3: Update NetBox configuration
Add the plugin to your NetBox `configuration.py`:
```python
PLUGINS = [
    'netbox_scion',
]
```

### Step 4: Run migrations and restart
```bash
# Run migrations
docker-compose exec netbox /opt/netbox/venv/bin/python /opt/netbox/netbox/manage.py migrate

# Restart NetBox
docker-compose restart netbox
```

## Method 2: Using Volume Mount for Development

### Step 1: Create a volume mount in your docker-compose.yml
```yaml
services:
  netbox:
    # ... existing configuration
    volumes:
      - ./plugins/netbox_scion:/opt/netbox/netbox/plugins/netbox_scion:ro
      # ... other volumes
```

### Step 2: Copy the plugin source code
```bash
# Create plugins directory on your NetBox host
mkdir -p /path/to/your/netbox/plugins

# Copy the entire plugin directory
scp -r netbox_scion/ your-server:/path/to/your/netbox/plugins/
```

### Step 3: Update configuration and restart
```python
# In configuration.py
PLUGINS = [
    'netbox_scion',
]
```

```bash
# Restart NetBox
docker-compose restart netbox

# Run migrations
docker-compose exec netbox python manage.py migrate
```

## Method 3: Custom Docker Image (Production)

### Step 1: Create a Dockerfile extension
```dockerfile
FROM netboxcommunity/netbox:latest

# Copy and install the plugin
COPY dist/netbox_scion-0.1.0-py3-none-any.whl /tmp/
RUN pip install /tmp/netbox_scion-0.1.0-py3-none-any.whl && rm /tmp/netbox_scion-0.1.0-py3-none-any.whl

# Copy custom configuration if needed
# COPY configuration.py /etc/netbox/config/configuration.py
```

### Step 2: Build and deploy
```bash
# Build custom image
docker build -t your-registry/netbox-scion:latest .

# Update docker-compose.yml to use your custom image
# services:
#   netbox:
#     image: your-registry/netbox-scion:latest
```

## Method 4: Git Clone Method

### Step 1: Clone directly in container
```bash
# Clone the repo in the container
docker-compose exec netbox git clone https://github.com/aciupac/netbox-scion.git /tmp/netbox-scion

# Install in development mode
docker-compose exec netbox pip install -e /tmp/netbox-scion
```

## Configuration

Regardless of the installation method, you need to:

1. **Add to PLUGINS** in `configuration.py`:
```python
PLUGINS = [
    'netbox_scion',
]

# Optional plugin configuration
PLUGINS_CONFIG = {
    'netbox_scion': {
        # Plugin-specific settings (none required currently)
    }
}
```

2. **Run migrations**:
```bash
docker-compose exec netbox python manage.py migrate
```

3. **Restart NetBox**:
```bash
docker-compose restart netbox
```

## Verification

After installation, verify the plugin is working:

1. **Check installed plugins**:
```bash
docker-compose exec netbox python manage.py shell -c "from django.conf import settings; print(settings.PLUGINS)"
```

2. **Access the web interface**:
   - Navigate to your NetBox URL
   - Look for "SCION" in the main navigation menu
   - You should see: Organizations, ISD-ASes, SCION Link Assignments

3. **Test the API**:
```bash
curl -H "Authorization: Token YOUR_TOKEN" \
     http://your-netbox-url/api/plugins/scion/organizations/
```

## Troubleshooting

### Common Issues:

1. **Plugin not appearing in menu**:
   - Ensure `netbox_scion` is in PLUGINS list
   - Restart NetBox container
   - Check logs: `docker-compose logs netbox`

2. **Migration errors**:
   - Ensure database permissions are correct
   - Run: `docker-compose exec netbox python manage.py showmigrations netbox_scion`

3. **Import errors**:
   - Verify plugin is installed: `docker-compose exec netbox pip list | grep netbox-scion`
   - Check Python path: `docker-compose exec netbox python -c "import netbox_scion; print(netbox_scion.__file__)"`

### Log Locations:
- NetBox logs: `docker-compose logs netbox`
- Django logs: Inside container at `/opt/netbox/netbox/logs/`

## Recommended Deployment for Production

For production environments, use **Method 1** (wheel package) or **Method 3** (custom Docker image) as they provide better isolation and version control.

For development and testing, **Method 2** (volume mount) is most convenient as it allows real-time code changes.
