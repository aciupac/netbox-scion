#!/bin/bash

# NetBox SCION Plugin Deployment Script
# This script helps deploy the plugin to a Docker-based NetBox installation

set -e

# Configuration
PLUGIN_NAME="netbox_scion"
WHEEL_FILE="netbox_scion-0.1.0-py3-none-any.whl"
CONTAINER_NAME="netbox"  # Adjust if your container has a different name

echo "🚀 NetBox SCION Plugin Deployment Script"
echo "========================================"

# Function to check if Docker is available
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker is not installed or not in PATH"
        exit 1
    fi
    echo "✅ Docker is available"
}

# Function to check if docker-compose is available
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        COMPOSE_CMD="docker-compose"
    elif docker compose version &> /dev/null; then
        COMPOSE_CMD="docker compose"
    else
        echo "❌ Neither docker-compose nor 'docker compose' is available"
        exit 1
    fi
    echo "✅ Docker Compose is available: $COMPOSE_CMD"
}

# Function to install via wheel package
install_wheel() {
    echo "📦 Installing plugin via wheel package..."
    
    if [ ! -f "dist/$WHEEL_FILE" ]; then
        echo "❌ Wheel file not found: dist/$WHEEL_FILE"
        echo "Run 'python setup.py bdist_wheel' first"
        exit 1
    fi
    
    # Copy wheel to container
    docker cp "dist/$WHEEL_FILE" "$CONTAINER_NAME:/tmp/"
    
    # Install the wheel
    docker exec "$CONTAINER_NAME" pip install "/tmp/$WHEEL_FILE"
    
    # Clean up
    docker exec "$CONTAINER_NAME" rm "/tmp/$WHEEL_FILE"
    
    echo "✅ Plugin installed via wheel package"
}

# Function to install via source mount
install_source() {
    echo "📂 Installing plugin via source mount..."
    
    # Check if docker-compose.yml exists
    if [ ! -f "docker-compose.yml" ]; then
        echo "❌ docker-compose.yml not found"
        echo "Please ensure you're in the right directory or use the wheel installation method"
        exit 1
    fi
    
    echo "✅ Plugin source will be mounted on next container restart"
}

# Function to run migrations
run_migrations() {
    echo "🔄 Running database migrations..."
    
    if command -v $COMPOSE_CMD &> /dev/null; then
        $COMPOSE_CMD exec netbox python manage.py migrate
    else
        docker exec "$CONTAINER_NAME" python manage.py migrate
    fi
    
    echo "✅ Migrations completed"
}

# Function to restart NetBox
restart_netbox() {
    echo "🔄 Restarting NetBox..."
    
    if command -v $COMPOSE_CMD &> /dev/null; then
        $COMPOSE_CMD restart netbox
    else
        docker restart "$CONTAINER_NAME"
    fi
    
    echo "✅ NetBox restarted"
}

# Function to verify installation
verify_installation() {
    echo "🔍 Verifying installation..."
    
    # Wait a moment for NetBox to start
    sleep 5
    
    # Check if plugin is installed
    if docker exec "$CONTAINER_NAME" pip list | grep -q netbox-scion; then
        echo "✅ Plugin package is installed"
    else
        echo "⚠️  Plugin package not found in pip list"
    fi
    
    # Check if plugin is importable
    if docker exec "$CONTAINER_NAME" python -c "import netbox_scion; print('Plugin version:', netbox_scion.__version__)" 2>/dev/null; then
        echo "✅ Plugin is importable"
    else
        echo "❌ Plugin import failed"
    fi
    
    echo ""
    echo "🎉 Deployment complete!"
    echo ""
    echo "Next steps:"
    echo "1. Add 'netbox_scion' to PLUGINS in your configuration.py"
    echo "2. Access your NetBox web interface"
    echo "3. Look for 'SCION' in the main navigation menu"
    echo "4. Check the API at: /api/plugins/scion/"
}

# Main deployment logic
main() {
    echo "Select deployment method:"
    echo "1) Install via wheel package (recommended for production)"
    echo "2) Install via source mount (recommended for development)"
    echo "3) Just run migrations and restart (if already installed)"
    echo ""
    read -p "Enter your choice (1-3): " choice
    
    check_docker
    check_docker_compose
    
    case $choice in
        1)
            install_wheel
            run_migrations
            restart_netbox
            verify_installation
            ;;
        2)
            install_source
            run_migrations
            restart_netbox
            verify_installation
            ;;
        3)
            run_migrations
            restart_netbox
            verify_installation
            ;;
        *)
            echo "❌ Invalid choice"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
