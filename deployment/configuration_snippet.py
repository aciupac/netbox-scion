# NetBox SCION Plugin Configuration
# Add this to your NetBox configuration.py file

# Add the plugin to your PLUGINS list
PLUGINS = [
    'netbox_scion',
    # ... your other plugins
]

# Optional: Plugin-specific configuration
PLUGINS_CONFIG = {
    'netbox_scion': {
        # No specific configuration required currently
        # Future configuration options will be documented here
    }
}

# Optional: Add custom logging for the plugin
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/opt/netbox/logs/netbox_scion.log',
        },
    },
    'loggers': {
        'netbox_scion': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
