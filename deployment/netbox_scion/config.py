from netbox.plugins import PluginConfig


class NetBoxScionConfig(PluginConfig):
    name = 'netbox_scion'
    verbose_name = 'NetBox SCION'
    description = 'NetBox plugin for managing SCION Links Assignment'
    version = '0.1.0'
    author = 'Your Name'
    author_email = 'your.email@example.com'
    base_url = 'scion'
    required_settings = []
    default_settings = {}


config = NetBoxScionConfig
