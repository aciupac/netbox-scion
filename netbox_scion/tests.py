from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Organization, ISDAS, SCIONLinkAssignment


class OrganizationTestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            short_name="ACME",
            full_name="ACME Corporation",
            description="Test organization"
        )

    def test_organization_str(self):
        """Test Organization string representation"""
        self.assertEqual(str(self.organization), "ACME")

    def test_organization_unique_short_name(self):
        """Test that short_name must be unique"""
        with self.assertRaises(Exception):
            Organization.objects.create(
                short_name="ACME",  # Duplicate
                full_name="Another ACME",
            )


class ISDATestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            short_name="ACME",
            full_name="ACME Corporation"
        )
        self.isdas = ISDAS.objects.create(
            isd_as="1-ff00:0:110",
            organization=self.organization,
            appliances=["core1.example.com", "core2.example.com"],
            description="Test ISD-AS"
        )

    def test_isdas_str(self):
        """Test ISDAS string representation"""
        self.assertEqual(str(self.isdas), "1-ff00:0:110")

    def test_isdas_appliances_display(self):
        """Test appliances display property"""
        expected = "core1.example.com, core2.example.com"
        self.assertEqual(self.isdas.appliances_display, expected)

    def test_invalid_isd_as_format(self):
        """Test that invalid ISD-AS format raises validation error"""
        with self.assertRaises(ValidationError):
            isdas = ISDAS(
                isd_as="invalid-format",
                organization=self.organization
            )
            isdas.full_clean()


class SCIONLinkAssignmentTestCase(TestCase):
    def setUp(self):
        self.organization = Organization.objects.create(
            short_name="ACME",
            full_name="ACME Corporation"
        )
        self.isdas = ISDAS.objects.create(
            isd_as="1-ff00:0:110",
            organization=self.organization
        )
        self.assignment = SCIONLinkAssignment.objects.create(
            isd_as=self.isdas,
            core="v1",
            interface_id=1,
            relationship=SCIONLinkAssignment.RELATIONSHIP_CHILD,
            customer_id="customer1",
            peer_name="Customer Corp",
            peer="customer-corp-peer",
            ticket="12345"
        )

    def test_assignment_str(self):
        """Test SCIONLinkAssignment string representation"""
        expected = "1-ff00:0:110 - Interface 1"
        self.assertEqual(str(self.assignment), expected)

    def test_ticket_field(self):
        """Test ticket field persists"""
        self.assertEqual(self.assignment.ticket, "12345")

    def test_unique_interface_per_isdas(self):
        """Test that interface_id must be unique per ISD-AS"""
        with self.assertRaises(Exception):
            SCIONLinkAssignment.objects.create(
                isd_as=self.isdas,
                interface_id=1,  # Duplicate
                customer_id="CUST002",
                peer_name="Another Customer",
                peer="another-customer-peer",
                zendesk_ticket="54321"
            )

    def test_invalid_zendesk_ticket(self):
        """Test that non-numeric Zendesk ticket raises validation error"""
        with self.assertRaises(ValidationError):
            assignment = SCIONLinkAssignment(
                isd_as=self.isdas,
                interface_id=2,
                customer_id="CUST002",
                peer_name="Customer Corp",
                peer="customer-corp-peer",
                ticket="not-a-number"
            )
            assignment.full_clean()


class ChangeLogViewTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="testuser",
            password="testpass",
            email="test@example.com"
        )
        self.user.is_staff = True
        self.user.is_superuser = True
        self.user.save()
        self.client.force_login(self.user)

        self.organization = Organization.objects.create(
            short_name="ACME",
            full_name="ACME Corporation"
        )
        self.isdas = ISDAS.objects.create(
            isd_as="1-ff00:0:200",
            organization=self.organization
        )
        self.assignment = SCIONLinkAssignment.objects.create(
            isd_as=self.isdas,
            core="core1",
            interface_id=10,
            relationship=SCIONLinkAssignment.RELATIONSHIP_CHILD
        )

    def test_organization_changelog_view(self):
        url = reverse('plugins:netbox_scion:organization_changelog', kwargs={'pk': self.organization.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_isdas_changelog_view(self):
        url = reverse('plugins:netbox_scion:isdas_changelog', kwargs={'pk': self.isdas.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_link_assignment_changelog_view(self):
        url = reverse('plugins:netbox_scion:scionlinkassignment_changelog', kwargs={'pk': self.assignment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
