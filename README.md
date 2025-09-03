# NetBox SCION Plugin

A comprehensive NetBox plugin for managing SCION (Scalability, Control, and Isolation On Next-generation networks) infrastructure.

**📦 Available on PyPI:** `pip install netbox-scion`

## 🚀 Quick Start

### Prerequisites
- NetBox deployment using netbox-docker
- Docker and Docker Compose

### Installation

**Method 1: PyPI Installation (Recommended)**
```bash
# Copy deployment files
cp -r deployment/* /path/to/your/netbox-docker/

# Use the PyPI Dockerfile
cp Dockerfile.netbox-pip /path/to/your/netbox-docker/

# Update docker-compose.yml
# dockerfile: Dockerfile.netbox-pip

```

**Method 2: Local Installation**
```bash
# Copy deployment files
cp -r deployment/* /path/to/your/netbox-docker/
```

**Configuration:**

1. **Update docker-compose.yml:**
```yaml
services:
  netbox:
    build:
      context: .
      dockerfile: Dockerfile.netbox-pip  # For PyPI installation
```

2. **Add to your NetBox plugins.py:**
```python
PLUGINS = [
    'netbox_scion',
    # Your existing plugins...
]
```

3. **Add to your env/netbox.env:**
```bash
PLUGINS_REQUIREMENTS=netbox-scion==1.0.0
```

4. **Deploy:**
```bash
cd /path/to/your/netbox-docker
docker-compose down
docker-compose build --no-cache netbox
docker-compose up -d
```

**Method 2: Local Installation**#### Option 1: PyPI Package (Recommended)
```bash
# Install directly from PyPI
pip install netbox-scion==1.0.0

# Or use our Docker deployment with pip installation
cp deployment/Dockerfile.netbox-pip /path/to/your/netbox-docker/
cp deployment/plugin_requirements.txt /path/to/your/netbox-docker/
```

#### Option 2: Local Development
**Method 2: Local Installation**
```bash
# Copy deployment files
cp -r deployment/* /path/to/your/netbox-docker/
```

**Configuration:**

4. Add to your `env/netbox.env`:
```bash
PLUGINS_REQUIREMENTS=netbox-scion==1.0.0
```

5. Deploy:
```bash
cd /path/to/your/netbox-docker
docker-compose down
docker-compose build --no-cache netbox
docker-compose up -d
```

See [deployment/README.md](deployment/README.md) for detailed instructions.

## 🏗️ Features

### Organizations
- Manage SCION organizations with short and full names
- Description and metadata fields
- REST API and export capabilities

### ISD-ASes (Isolation Domain - Autonomous System)
- ISD-AS identifier management with regex validation (`^\d+-[0-9a-f]{1,4}:[0-9a-f]{1,4}:[0-9a-f]{1,4}$`)
- Organization association
- Core nodes list support
- Detailed descriptions

### SCION Link Assignments
- Interface assignment management (interface_id per ISD-AS must be unique)
- Customer information (ID and name)
- Zendesk ticket integration
- Advanced filtering and search capabilities

## 🎯 Navigation

Plugin appears under the "Plugins" section in NetBox sidebar with:
- Organizations
- ISD-ASes
- SCION Link Assignments

## 🔧 API Endpoints

- Organizations: `/api/plugins/scion/organizations/`
- ISD-ASes: `/api/plugins/scion/isd-ases/`
- Link Assignments: `/api/plugins/scion/link-assignments/`

All endpoints support full CRUD operations with filtering, pagination, and export.

## 📁 Development

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

## 🐛 Support

For issues, please check:
1. Plugin installation: `docker exec netbox /opt/netbox/venv/bin/pip list | grep netbox-scion`
2. Configuration: Plugin in `PLUGINS` list and `PLUGINS_REQUIREMENTS`
3. Migrations: Auto-handled by custom entrypoint script
4. Restart NetBox container if needed

## 📝 License

Apache License 2.0
