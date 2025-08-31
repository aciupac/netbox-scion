from netbox.views import generic
from . import forms, models, tables, filtersets


class OrganizationView(generic.ObjectView):
    queryset = models.Organization.objects.all()


class OrganizationListView(generic.ObjectListView):
    queryset = models.Organization.objects.all()
    table = tables.OrganizationTable
    filterset = filtersets.OrganizationFilterSet


class OrganizationEditView(generic.ObjectEditView):
    queryset = models.Organization.objects.all()
    form = forms.OrganizationForm


class OrganizationDeleteView(generic.ObjectDeleteView):
    queryset = models.Organization.objects.all()


class ISDAView(generic.ObjectView):
    queryset = models.ISDAS.objects.select_related('organization')


class ISDAListView(generic.ObjectListView):
    queryset = models.ISDAS.objects.select_related('organization').prefetch_related('link_assignments')
    table = tables.ISDATable
    filterset = filtersets.ISDAFilterSet


class ISDAEditView(generic.ObjectEditView):
    queryset = models.ISDAS.objects.all()
    form = forms.ISDAForm


class ISDADeleteView(generic.ObjectDeleteView):
    queryset = models.ISDAS.objects.all()


class SCIONLinkAssignmentView(generic.ObjectView):
    queryset = models.SCIONLinkAssignment.objects.select_related('isd_as', 'isd_as__organization')


class SCIONLinkAssignmentListView(generic.ObjectListView):
    queryset = models.SCIONLinkAssignment.objects.select_related('isd_as', 'isd_as__organization')
    table = tables.SCIONLinkAssignmentTable
    filterset = filtersets.SCIONLinkAssignmentFilterSet


class SCIONLinkAssignmentEditView(generic.ObjectEditView):
    queryset = models.SCIONLinkAssignment.objects.all()
    form = forms.SCIONLinkAssignmentForm


class SCIONLinkAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = models.SCIONLinkAssignment.objects.all()
