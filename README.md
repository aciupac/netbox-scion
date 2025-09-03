# NetBox SCION Plugin

A comprehensive NetBox plugin for managing SCION (Scalability, Control, and Isolation On Next-generation networks) infrastructure.

[![PyPI](https://img.shields.io/pypi/v/netbox-scion)](https://pypi.org/project/netbox-scion/)
[![Python Version](https://img.shields.io/pypi/pyversions/netbox-scion)](https://pypi.org/project/netbox-scion/)
[![License](https://img.shields.io/github/license/aciupac/netbox-scion)](https://github.com/aciupac/netbox-scion/blob/main/LICENSE)

## ✨ Features

- **Organizations:** Manage SCION operators with metadata and descriptions
- **ISD-ASes:** Track Isolation Domain and Autonomous System identifiers with core nodes
- **Link Assignments:** Interface management with customer information and Zendesk integration
- **REST API:** Full CRUD operations with filtering and pagination
- **Export:** CSV and Excel export capabilities
- **Web Interface:** Advanced filtering and search capabilities

## 📦 Installation

```bash
pip install netbox-scion
```

## 🚀 Quick Start

### Prerequisites
- NetBox v4.0+ deployed using [netbox-docker](https://github.com/netbox-community/netbox-docker)
- Docker and Docker Compose

### Installation

The NetBox SCION plugin can be installed directly from PyPI without cloning this repository.

#### Method 1: Environment Variables (Recommended)

Add the plugin to your NetBox environment:

**1. Update your `env/netbox.env` file:**
```bash
# Add to existing PLUGINS_REQUIREMENTS or create new line
PLUGINS_REQUIREMENTS=netbox-scion==1.0.0
```

**2. Add to your `configuration/plugins.py` file:**
```python
PLUGINS = [
    'netbox_scion',
    # Your other existing plugins...
]
```

**3. Restart NetBox:**
```bash
cd /path/to/your/netbox-docker
docker-compose restart netbox netbox-worker
```

#### Method 2: Custom Docker Image

For more control or if you need additional customizations:

**1. Create a custom Dockerfile:**
```dockerfile
FROM netboxcommunity/netbox:v4.3-3.3.0

# Install the plugin
RUN /opt/netbox/venv/bin/pip install netbox-scion==1.0.0
```

**2. Update your `docker-compose.yml`:**
```yaml
services:
  netbox: &netbox
    build:
      context: .
      dockerfile: Dockerfile  # Your custom Dockerfile
    # Remove the 'image:' line
```

**3. Add plugin configuration and rebuild:**
```bash
cd /path/to/your/netbox-docker
docker-compose down
docker-compose build --no-cache netbox
docker-compose up -d
```

### Verification

Check that the plugin is installed correctly:

```bash
# Verify installation
docker exec netbox /opt/netbox/venv/bin/pip show netbox-scion

# Check plugin is loaded
docker logs netbox | grep -i scion
```

The plugin will appear under "Plugins" in the NetBox sidebar with Organizations, ISD-ASes, and SCION Link Assignments.

## 🔧 API Endpoints

All endpoints support full CRUD operations with filtering, pagination, and export:

- **Organizations:** `/api/plugins/scion/organizations/`
- **ISD-ASes:** `/api/plugins/scion/isd-ases/`
- **Link Assignments:** `/api/plugins/scion/link-assignments/`

## 🎯 Navigation

The plugin adds a "Plugins" section to the NetBox sidebar with:
- Organizations
- ISD-ASes  
- SCION Link Assignments

## 📁 Development

### For Plugin Users
Most users only need to install via pip (see Installation above). No need to clone this repository.

### For Developers

If you want to contribute or customize the plugin:

```bash
# Clone the repository
git clone https://github.com/aciupac/netbox-scion.git
cd netbox-scion

# Install in development mode
pip install -e .

# Or use the deployment files for testing
cp -r deployment/* /path/to/your/netbox-docker/
```

### Project Structure
```
netbox_scion/
├── __init__.py              # Plugin configuration
├── models.py                # Data models
├── forms.py                 # Web forms
├── views.py                 # Web views
├── urls.py                  # URL routing
├── api/                     # REST API
├── templates/               # HTML templates
├── migrations/              # Database migrations
└── static/                  # CSS/JS assets
```

### Local Development
```bash
# Install in development mode
pip install -e .

# Run migrations
python manage.py migrate

# Create wheel package
python setup.py bdist_wheel
```

## 🐛 Troubleshooting

### Plugin Not Appearing
1. **Check installation:**
   ```bash
   docker exec netbox /opt/netbox/venv/bin/pip show netbox-scion
   ```

2. **Verify configuration:**
   - Plugin in `PLUGINS` list in `configuration/plugins.py`
   - Plugin in `PLUGINS_REQUIREMENTS` in `env/netbox.env`

3. **Check logs:**
   ```bash
   docker logs netbox | grep -i error
   docker logs netbox | grep -i scion
   ```

4. **Restart services:**
   ```bash
   docker-compose restart netbox netbox-worker
   ```

### Database Issues
- Migrations run automatically with netbox-docker
- For manual migration: `docker exec netbox python manage.py migrate`

### Getting Help
- 🐛 **Bug reports:** [GitHub Issues](https://github.com/aciupac/netbox-scion/issues)
- 💬 **Questions:** [GitHub Discussions](https://github.com/aciupac/netbox-scion/discussions)
- 📚 **Documentation:** [deployment/README.md](deployment/README.md)

## 📝 License

Apache License 2.0
