from django import forms
from netbox.forms import NetBoxModelForm
from .models import Organization, ISDAS, SCIONLinkAssignment

try:
    from django.contrib.postgres.fields import ArrayField
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False


class MultipleStringWidget(forms.Widget):
    """
    Custom widget for handling multiple strings as a textarea
    """
    def __init__(self, attrs=None):
        super().__init__(attrs)
        if 'class' not in (attrs or {}):
            self.attrs = {'class': 'form-control'}

    def format_value(self, value):
        if value is None:
            return ''
        if isinstance(value, list):
            return '\n'.join(value)
        return value

    def value_from_datadict(self, data, files, name):
        value = data.get(name, '')
        if value:
            return [line.strip() for line in value.split('\n') if line.strip()]
        return []


class MultipleStringField(forms.Field):
    """
    Custom field for handling multiple strings
    """
    widget = MultipleStringWidget

    def __init__(self, **kwargs):
        kwargs.setdefault('widget', MultipleStringWidget(attrs={'rows': 4}))
        super().__init__(**kwargs)

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        if isinstance(value, str):
            return [line.strip() for line in value.split('\n') if line.strip()]
        return []

    def validate(self, value):
        super().validate(value)
        if value and not isinstance(value, list):
            raise forms.ValidationError('Invalid format for multiple strings')


class OrganizationForm(NetBoxModelForm):
    class Meta:
        model = Organization
        fields = ('short_name', 'full_name', 'description')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ISDAForm(NetBoxModelForm):
    if not POSTGRES_AVAILABLE:
        cores = MultipleStringField(
            required=False,
            help_text="Enter one core per line",
            label="Cores"
        )

    class Meta:
        model = ISDAS
        fields = ('isd_as', 'description', 'organization', 'cores')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        if POSTGRES_AVAILABLE:
            widgets['cores'] = forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Enter one core per line'
            })

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if POSTGRES_AVAILABLE and self.instance and self.instance.pk:
            # For PostgreSQL ArrayField, convert list to textarea format
            if self.instance.cores:
                self.initial['cores'] = '\n'.join(self.instance.cores)

    def clean_cores(self):
        cores = self.cleaned_data.get('cores')
        if POSTGRES_AVAILABLE and isinstance(cores, str):
            # Convert textarea input to list for PostgreSQL
            return [line.strip() for line in cores.split('\n') if line.strip()]
        return cores or []


class SCIONLinkAssignmentForm(NetBoxModelForm):
    class Meta:
        model = SCIONLinkAssignment
        fields = ('isd_as', 'interface_id', 'customer_id', 'customer_name', 'zendesk_ticket')

    def clean_zendesk_ticket(self):
        ticket = self.cleaned_data.get('zendesk_ticket')
        if ticket and not ticket.isdigit():
            raise forms.ValidationError("Zendesk ticket must contain only numbers")
        return ticket
