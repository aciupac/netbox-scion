import django_tables2 as tables
from django.utils.html import format_html
from netbox.tables import NetBoxTable, ChoiceFieldColumn
from .models import Organization, ISDAS, SCIONLinkAssignment


class OrganizationTable(NetBoxTable):
    short_name = tables.Column(
        linkify=True
    )
    full_name = tables.Column()
    isd_ases_count = tables.Column(
        accessor='isd_ases__count',
        verbose_name='ISD-ASes',
        orderable=False
    )

    class Meta(NetBoxTable.Meta):
        model = Organization
        fields = ('pk', 'id', 'short_name', 'full_name', 'description', 'isd_ases_count')
        default_columns = ('short_name', 'full_name', 'description', 'isd_ases_count')


class ISDATable(NetBoxTable):
    isd_as = tables.Column(
        linkify=True
    )
    organization = tables.Column(
        linkify=True
    )
    cores = tables.Column(
        accessor='cores_display',
        verbose_name='Cores',
        orderable=False
    )
    link_assignments_count = tables.Column(
        accessor='link_assignments__count',
        verbose_name='Link Assignments',
        orderable=False
    )

    class Meta(NetBoxTable.Meta):
        model = ISDAS
        fields = ('pk', 'id', 'isd_as', 'organization', 'description', 'cores', 'link_assignments_count')
        default_columns = ('isd_as', 'organization', 'description', 'cores', 'link_assignments_count')


class SCIONLinkAssignmentTable(NetBoxTable):
    isd_as = tables.Column(
        linkify=True
    )
    interface_id = tables.Column()
    customer_id = tables.Column()
    customer_name = tables.Column()
    zendesk_ticket = tables.Column(
        verbose_name='Zendesk Ticket'
    )

    class Meta(NetBoxTable.Meta):
        model = SCIONLinkAssignment
        fields = ('pk', 'id', 'isd_as', 'interface_id', 'customer_id', 'customer_name', 'zendesk_ticket')
        default_columns = ('isd_as', 'interface_id', 'customer_id', 'customer_name', 'zendesk_ticket')

    def render_zendesk_ticket(self, value, record):
        """Render Zendesk ticket as a clickable link"""
        if value:
            url = record.get_zendesk_url()
            return format_html('<a href="{}" target="_blank">{}</a>', url, value)
        return value
