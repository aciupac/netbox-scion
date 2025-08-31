FROM netboxcommunity/netbox:latest

LABEL maintainer="NetBox SCION Plugin"
LABEL description="NetBox with SCION plugin pre-installed"

# Copy and install the plugin wheel
COPY dist/netbox_scion-0.1.0-py3-none-any.whl /tmp/

# Install the plugin
RUN pip install /tmp/netbox_scion-0.1.0-py3-none-any.whl && \
    rm /tmp/netbox_scion-0.1.0-py3-none-any.whl

# Optional: Copy custom configuration template
# COPY deployment/configuration_snippet.py /etc/netbox/config/configuration_template.py

# Expose NetBox port
EXPOSE 8000

# Use the same entrypoint as the base image
# CMD and ENTRYPOINT are inherited from base image
