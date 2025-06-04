from django import forms
from django.db import transaction

from organization.models import Organization


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        exclude = ["user", "address", "is_verified"]
        labels = {
            "name": "Institute name",
            "website": "Institute website (if any)",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Please enter institute name"}
            ),
            "website": forms.URLInput(
                attrs={"placeholder": "Please enter institute website if available"}
            ),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(OrganizationForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.user = user

    @transaction.atomic
    def save(self, user=None, address=None, commit=True):
        organization = super().save(commit=False)

        if user:
            organization.user = user
        if address:
            organization.address = address

        if commit:
            organization.save()

        return organization
