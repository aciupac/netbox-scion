# Contributing to NetBox SCION Plugin

Thank you for your interest in contributing to the NetBox SCION plugin!

## How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or suggest features
- Provide clear reproduction steps for bugs
- Include your NetBox and Python versions

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/yourusername/netbox-scion.git`
3. Install in development mode: `pip install -e .`
4. Make your changes
5. Test your changes
6. Submit a pull request

### Building the Package
To build distribution packages:
```bash
# Build both source distribution and wheel
python setup.py sdist bdist_wheel

# Files will be created in dist/ directory:
# - netbox-scion-X.Y.Z.tar.gz (source distribution)
# - netbox_scion-X.Y.Z-py3-none-any.whl (wheel package)
```

### Local Testing
For local testing with NetBox, see the [Advanced Deployment Guide](deployment/README.md) which covers:
- Testing with local wheel files
- Custom Docker images for development
- Development environment setup
- Troubleshooting installation issues

### Production Deployment Testing
To test your changes in a production-like environment:
1. Build the package: `python setup.py bdist_wheel`
2. Copy wheel to your netbox-docker deployment
3. Add to `plugin_requirements.txt`
4. Use custom Dockerfile method (see README.md)
5. Test with `docker-compose build && docker-compose up -d`

### Code Style
- Follow Python PEP 8 style guidelines
- Use meaningful variable and function names
- Add comments for complex logic
- Update tests for new features

### Testing
Run tests before submitting:
```bash
python -m pytest netbox_scion/tests.py
```

### Pull Request Process
1. Update documentation if needed
2. Add or update tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Submit pull request with clear description

## Questions?
Feel free to open an issue for any questions about contributing.
