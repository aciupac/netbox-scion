import django_filters
from django.db import models
from netbox.filtersets import NetBoxModelFilterSet
from .models import Organization, ISDAS, SCIONLinkAssignment


class OrganizationFilterSet(NetBoxModelFilterSet):
    class Meta:
        model = Organization
        fields = ('id', 'short_name', 'full_name')

    def search(self, queryset, name, value):
        return queryset.filter(
            models.Q(short_name__icontains=value) |
            models.Q(full_name__icontains=value) |
            models.Q(description__icontains=value)
        )


class ISDAFilterSet(NetBoxModelFilterSet):
    organization_id = django_filters.ModelMultipleChoiceFilter(
        queryset=Organization.objects.all(),
        label='Organization (ID)',
    )
    organization = django_filters.ModelMultipleChoiceFilter(
        field_name='organization__short_name',
        queryset=Organization.objects.all(),
        to_field_name='short_name',
        label='Organization (name)',
    )

    class Meta:
        model = ISDAS
        fields = ('id', 'isd_as', 'organization')

    def search(self, queryset, name, value):
        return queryset.filter(
            models.Q(isd_as__icontains=value) |
            models.Q(description__icontains=value) |
            models.Q(organization__short_name__icontains=value) |
            models.Q(organization__full_name__icontains=value)
        )


class SCIONLinkAssignmentFilterSet(NetBoxModelFilterSet):
    isd_as_id = django_filters.ModelMultipleChoiceFilter(
        queryset=ISDAS.objects.all(),
        label='ISD-AS (ID)',
    )
    isd_as = django_filters.ModelMultipleChoiceFilter(
        field_name='isd_as__isd_as',
        queryset=ISDAS.objects.all(),
        to_field_name='isd_as',
        label='ISD-AS',
    )
    customer_id = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Customer ID (contains)',
    )
    customer_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Customer Name (contains)',
    )

    class Meta:
        model = SCIONLinkAssignment
        fields = ('id', 'isd_as', 'interface_id', 'customer_id', 'customer_name', 'zendesk_ticket')

    def search(self, queryset, name, value):
        return queryset.filter(
            models.Q(isd_as__isd_as__icontains=value) |
            models.Q(customer_id__icontains=value) |
            models.Q(customer_name__icontains=value) |
            models.Q(zendesk_ticket__icontains=value)
        )
