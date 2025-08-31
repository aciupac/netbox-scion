# NetBox SCION Plugin - Quick Start

This deployment package contains everything you need to install the NetBox SCION plugin.

## Contents

- `netbox_scion-0.1.0-py3-none-any.whl` - Plugin wheel package (recommended)
- `netbox_scion/` - Plugin source code (for development)
- `deploy.sh` - Automated deployment script
- `configuration_snippet.py` - Configuration to add to NetBox
- `docker-compose.yml` - Example Docker Compose setup
- `DOCKER_DEPLOYMENT.md` - Detailed deployment instructions

## Quick Installation

### Method 1: Automated Script (Recommended)
```bash
./deploy.sh
```

### Method 2: Manual Installation
```bash
# Copy wheel to your NetBox container
docker cp netbox_scion-0.1.0-py3-none-any.whl netbox:/tmp/

# Install the plugin
docker exec netbox pip install /tmp/netbox_scion-0.1.0-py3-none-any.whl

# Add to configuration.py:
# PLUGINS = ['netbox_scion']

# Run migrations
docker exec netbox python manage.py migrate

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

## Support

- GitHub: https://github.com/aciupac/netbox-scion
- Documentation: See DOCKER_DEPLOYMENT.md for detailed instructions
