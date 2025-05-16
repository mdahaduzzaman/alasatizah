from django import forms
from django.db import transaction

from organization.models import Organization


class OrganizationForm(forms.ModelForm):
    head_nid = forms.FileField(
        required=True,
        label="Head of the organization NID Front",
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"})
    )
    head_avatar = forms.FileField(
        required=True,
        label="Head of the organization photo",
        widget=forms.FileInput(attrs={"accept": "image/*"})
    )
    teacher_accomodation = forms.FileField(
        required=True,
        label="Ustaz accomodation photo",
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"})
    )
    meal_routine = forms.FileField(
        required=True,
        label="Ustaz meal routine",
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"})
    )
    hoilday_calendar = forms.FileField(
        required=True,
        label="Ustaz holiday calender photo",
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"})
    )
    committee_permission = forms.FileField(
        required=True,
        label="Organization committee permission",
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"})
    )
    pledge = forms.FileField(
        required=True,
        label="Pledge document",
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"})
    )
    class Meta:
        model = Organization
        exclude = ["user", "address", "is_verified"]
        labels = {
            "name": "Organization name",
            "email": "Organization email",
            "website": "Organization website (if any)",
            "facebook_page": "Organization facebook page (if any)",
            "youtube_page": "Organization youtube channel (if any)",
            "head_name": "Head of the organization Name",
            "rules": "Ustaz rules",
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
