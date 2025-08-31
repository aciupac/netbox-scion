from rest_framework import serializers
from netbox.api.serializers import NetBoxModelSerializer
from ..models import Organization, ISDAS, SCIONLinkAssignment


class OrganizationSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_scion-api:organization-detail'
    )
    isd_ases_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Organization
        fields = (
            'id', 'url', 'display', 'short_name', 'full_name', 'description',
            'isd_ases_count', 'created', 'last_updated'
        )


class ISDASerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_scion-api:isdas-detail'
    )
    organization = OrganizationSerializer(nested=True)
    link_assignments_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = ISDAS
        fields = (
            'id', 'url', 'display', 'isd_as', 'description', 'organization',
            'cores', 'link_assignments_count', 'created', 'last_updated'
        )


class SCIONLinkAssignmentSerializer(NetBoxModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='plugins-api:netbox_scion-api:scionlinkassignment-detail'
    )
    isd_as = ISDASerializer(nested=True, read_only=True)
    isd_as_id = serializers.IntegerField(write_only=True)
    zendesk_url = serializers.CharField(source='get_zendesk_url', read_only=True)

    class Meta:
        model = SCIONLinkAssignment
        fields = (
            'id', 'url', 'display', 'isd_as', 'isd_as_id', 'interface_id',
            'customer_id', 'customer_name', 'zendesk_ticket', 'zendesk_url',
            'created', 'last_updated'
        )
