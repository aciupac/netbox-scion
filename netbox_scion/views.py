from django.http import JsonResponse
from django.views.generic.base import RedirectView
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from netbox.views import generic
from . import forms, models, tables, filtersets


class PluginHomeView(generic.ObjectListView):
    """Home view for the SCION plugin showing all main sections."""
    queryset = models.SCIONLinkAssignment.objects.select_related('isd_as', 'isd_as__organization')
    table = tables.SCIONLinkAssignmentTable
    filterset = filtersets.SCIONLinkAssignmentFilterSet
    filterset_form = forms.SCIONLinkAssignmentFilterForm
    template_name = 'generic/object_list.html'


def get_isdas_appliances(request):
    """AJAX view to get appliances for a specific ISD-AS"""
    isdas_id = request.GET.get('isdas_id')
    
    if isdas_id:
        try:
            isdas = models.ISDAS.objects.get(pk=isdas_id)
            appliances = isdas.appliances or []
            
            return JsonResponse({
                'appliances': appliances
            })
        except models.ISDAS.DoesNotExist:
            return JsonResponse({
                'error': 'ISD-AS not found',
                'appliances': []
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'appliances': []
            })
    
    return JsonResponse({
        'error': 'No ISD-AS ID provided',
        'appliances': []
    })


class OrganizationView(generic.ObjectView):
    queryset = models.Organization.objects.prefetch_related('isd_ases')
    template_name = 'netbox_scion/organization_detail.html'


class OrganizationListView(generic.ObjectListView):
    queryset = models.Organization.objects.prefetch_related('isd_ases')
    table = tables.OrganizationTable
    filterset = filtersets.OrganizationFilterSet
    filterset_form = forms.OrganizationFilterForm


class OrganizationEditView(generic.ObjectEditView):
    queryset = models.Organization.objects.all()
    form = forms.OrganizationForm


class OrganizationDeleteView(generic.ObjectDeleteView):
    queryset = models.Organization.objects.all()


class OrganizationBulkDeleteView(generic.BulkDeleteView):
    queryset = models.Organization.objects.all()
    table = tables.OrganizationTable


class OrganizationChangeLogView(generic.ObjectChangeLogView):
    queryset = models.Organization.objects.all()
    model = models.Organization
    base_template = 'netbox_scion/organization_detail.html'


class ISDAView(generic.ObjectView):
    queryset = models.ISDAS.objects.select_related('organization')
    template_name = 'netbox_scion/isdas_detail.html'


class ISDAListView(generic.ObjectListView):
    queryset = models.ISDAS.objects.select_related('organization').prefetch_related('link_assignments')
    table = tables.ISDATable
    filterset = filtersets.ISDAFilterSet
    filterset_form = forms.ISDAFilterForm


class ISDAEditView(generic.ObjectEditView):
    queryset = models.ISDAS.objects.all()
    form = forms.ISDAForm


class ISDADeleteView(generic.ObjectDeleteView):
    queryset = models.ISDAS.objects.all()


class ISDABulkDeleteView(generic.BulkDeleteView):
    queryset = models.ISDAS.objects.all()
    table = tables.ISDATable


class ISDAChangeLogView(generic.ObjectChangeLogView):
    queryset = models.ISDAS.objects.all()
    model = models.ISDAS
    base_template = 'netbox_scion/isdas_detail.html'


def add_appliance_to_isdas(request, pk):
    """Add an appliance to an ISD-AS"""
    isdas = get_object_or_404(models.ISDAS, pk=pk)
    
    if request.method == 'POST':
        form = forms.ApplianceManagementForm(request.POST)
        if form.is_valid():
            appliance_name = form.cleaned_data['appliance_name']
            appliances = isdas.appliances or []
            
            if appliance_name not in appliances:
                appliances.append(appliance_name)
                isdas.appliances = appliances
                isdas.save()
                messages.success(request, f'Appliance "{appliance_name}" added successfully.')
            else:
                messages.error(request, f'Appliance "{appliance_name}" already exists.')
            
            return redirect('plugins:netbox_scion:isdas', pk=pk)
    else:
        form = forms.ApplianceManagementForm()
    
    return render(request, 'netbox_scion/add_core.html', {
        'form': form,
        'isdas': isdas,
        'return_url': request.GET.get('return_url', f"/plugins/scion/isdas/{pk}/"),
        'action': 'Add'
    })


def edit_appliance_in_isdas(request, pk, appliance_name):
    """Edit an appliance name in an ISD-AS"""
    isdas = get_object_or_404(models.ISDAS, pk=pk)
    appliances = isdas.appliances or []
    
    if appliance_name not in appliances:
        messages.error(request, f'Appliance "{appliance_name}" not found.')
        return redirect('plugins:netbox_scion:isdas', pk=pk)
    
    if request.method == 'POST':
        form = forms.ApplianceManagementForm(request.POST)
        if form.is_valid():
            new_appliance_name = form.cleaned_data['appliance_name']
            
            if new_appliance_name != appliance_name:
                if new_appliance_name in appliances:
                    messages.error(request, f'Appliance "{new_appliance_name}" already exists.')
                else:
                    # Update appliance name in the list
                    appliance_index = appliances.index(appliance_name)
                    appliances[appliance_index] = new_appliance_name
                    isdas.appliances = appliances
                    isdas.save()
                    
                    # Update all SCION link assignments that use this appliance
                    assignments = models.SCIONLinkAssignment.objects.filter(
                        isd_as=isdas, core=appliance_name
                    )
                    assignments.update(core=new_appliance_name)
                    
                    messages.success(request, f'Appliance renamed from "{appliance_name}" to "{new_appliance_name}".')
            else:
                messages.info(request, 'No changes made.')
            
            return redirect('plugins:netbox_scion:isdas', pk=pk)
    else:
        form = forms.ApplianceManagementForm(initial={'appliance_name': appliance_name})
    
    return render(request, 'netbox_scion/add_core.html', {
        'form': form,
        'isdas': isdas,
        'return_url': request.GET.get('return_url', f"/plugins/scion/isdas/{pk}/"),
        'action': 'Edit',
        'appliance_name': appliance_name
    })


def remove_appliance_from_isdas(request, pk, appliance_name):
    """Remove an appliance from an ISD-AS and all associated SCION link assignments"""
    isdas = get_object_or_404(models.ISDAS, pk=pk)
    
    appliances = isdas.appliances or []
    if appliance_name in appliances:
        # Check how many SCION link assignments will be deleted
        assignments_to_delete = models.SCIONLinkAssignment.objects.filter(
            isd_as=isdas, core=appliance_name
        )
        assignments_count = assignments_to_delete.count()
        
        # Remove the appliance
        appliances.remove(appliance_name)
        isdas.appliances = appliances
        isdas.save()
        
        # Delete all associated SCION link assignments
        if assignments_count > 0:
            assignments_to_delete.delete()
            messages.warning(
                request, 
                f'Appliance "{appliance_name}" removed successfully. '
                f'{assignments_count} SCION link assignment(s) were also deleted.'
            )
        else:
            messages.success(request, f'Appliance "{appliance_name}" removed successfully.')
    else:
        messages.error(request, f'Appliance "{appliance_name}" not found.')
    
    return redirect('plugins:netbox_scion:isdas', pk=pk)


class SCIONLinkAssignmentView(generic.ObjectView):
    queryset = models.SCIONLinkAssignment.objects.select_related('isd_as', 'isd_as__organization')
    template_name = 'netbox_scion/scionlinkassignment_detail.html'


class SCIONLinkAssignmentListView(generic.ObjectListView):
    queryset = models.SCIONLinkAssignment.objects.select_related('isd_as', 'isd_as__organization')
    table = tables.SCIONLinkAssignmentTable
    filterset = filtersets.SCIONLinkAssignmentFilterSet
    filterset_form = forms.SCIONLinkAssignmentFilterForm


class SCIONLinkAssignmentEditView(generic.ObjectEditView):
    queryset = models.SCIONLinkAssignment.objects.all()
    form = forms.SCIONLinkAssignmentForm
    template_name = 'netbox_scion/scionlinkassignment_edit.html'
    
    def get_extra_addanother_params(self, request):
        """
        Return extra parameters to pass when redirecting to the create form 
        after clicking 'Create & Add Another'.
        """
        params = {}
        
        # Get the object that was just created
        if hasattr(self, 'object') and self.object:
            # Pre-fill ISD-AS
            if self.object.isd_as:
                params['isd_as'] = self.object.isd_as.pk
            
            # Calculate next interface_id
            next_interface_id = self.object.interface_id + 1
            
            # Check if that interface_id already exists, increment until we find a free one
            while models.SCIONLinkAssignment.objects.filter(
                isd_as=self.object.isd_as, 
                interface_id=next_interface_id
            ).exists():
                next_interface_id += 1
            
            params['interface_id'] = next_interface_id
        
        return params
    
    def get_return_url(self, request, obj=None):
        """
        Override to handle 'Create & Add Another' button.
        When user clicks that button, return to the create form with pre-filled values.
        """
        # Check if "Create & Add Another" was clicked
        if '_addanother' in request.POST and obj:
            # Set the object so get_extra_addanother_params can use it
            self.object = obj
            
            # Get extra parameters
            params = self.get_extra_addanother_params(request)
            
            # Build URL with pre-filled query parameters
            from django.urls import reverse
            base_url = reverse('plugins:netbox_scion:scionlinkassignment_add')
            
            if params:
                query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
                return f'{base_url}?{query_string}'
            
            return base_url
        
        # Default behavior for other buttons
        return super().get_return_url(request, obj)


class SCIONLinkAssignmentDeleteView(generic.ObjectDeleteView):
    queryset = models.SCIONLinkAssignment.objects.all()


class SCIONLinkAssignmentBulkDeleteView(generic.BulkDeleteView):
    queryset = models.SCIONLinkAssignment.objects.all()
    table = tables.SCIONLinkAssignmentTable


class SCIONLinkAssignmentChangeLogView(generic.ObjectChangeLogView):
    queryset = models.SCIONLinkAssignment.objects.all()
    model = models.SCIONLinkAssignment
    base_template = 'netbox_scion/scionlinkassignment_detail.html'
