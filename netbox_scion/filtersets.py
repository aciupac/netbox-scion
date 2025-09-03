import django_filters
from django_filters import FilterSet
from .models import Organization, ISDAS, SCIONLinkAssignment


class OrganizationFilterSet(FilterSet):
    class Meta:
        model = Organization
        fields = ['id', 'short_name', 'full_name']


class ISDAFilterSet(FilterSet):
    organization = django_filters.ModelMultipleChoiceFilter(
        queryset=Organization.objects.all(),
        label='Organization',
    )

    class Meta:
        model = ISDAS
        fields = ['id', 'isd_as', 'organization']


class SCIONLinkAssignmentFilterSet(FilterSet):
    isd_as = django_filters.ModelMultipleChoiceFilter(
        queryset=ISDAS.objects.all(),
        label='ISD-AS',
    )

    class Meta:
        model = SCIONLinkAssignment
        fields = ['id', 'isd_as', 'interface_id', 'customer_id', 'customer_name', 'zendesk_ticket']
