from netbox.api.viewsets import NetBoxModelViewSet
from django.db.models import Count
from .. import filtersets, models
from .serializers import OrganizationSerializer, ISDASerializer, SCIONLinkAssignmentSerializer


class OrganizationViewSet(NetBoxModelViewSet):
    queryset = models.Organization.objects.prefetch_related('isd_ases').annotate(
        isd_ases_count=Count('isd_ases')
    )
    serializer_class = OrganizationSerializer
    filterset_class = filtersets.OrganizationFilterSet


class ISDAViewSet(NetBoxModelViewSet):
    queryset = models.ISDAS.objects.select_related('organization').prefetch_related('link_assignments').annotate(
        link_assignments_count=Count('link_assignments')
    )
    serializer_class = ISDASerializer
    filterset_class = filtersets.ISDAFilterSet


class SCIONLinkAssignmentViewSet(NetBoxModelViewSet):
    queryset = models.SCIONLinkAssignment.objects.select_related('isd_as', 'isd_as__organization')
    serializer_class = SCIONLinkAssignmentSerializer
    filterset_class = filtersets.SCIONLinkAssignmentFilterSet
