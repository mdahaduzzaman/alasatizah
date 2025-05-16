from django import forms
from django.utils import timezone
from django.db import transaction


from ustaz.models import (
    Ustaz,
    EducationalQualification,
    TrainingCertificate,
    AchievementCertificate,
    OrganizationTestimonial,
)
from core.models import Address
from alasatizah.forms.fields import MultipleFileField


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["id"]


class UstazForm(forms.ModelForm):
    education_files = MultipleFileField(
        required=False,
        label="Educational Qualification Documents (Upload multiple files if available)",
    )

    training_files = MultipleFileField(
        required=False,
        label="Training Certificates (Upload multiple files if available)",
    )

    achievement_files = MultipleFileField(
        required=False,
        label="Achievement Certificates (Upload multiple files if available)",
    )

    testimonial_files = MultipleFileField(
        required=False,
        label="Organization Testimonials (Upload multiple files if available)",
    )
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    guardian_permission_letter = forms.FileField(
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"}),
        required=True
    )

    chairman_certificate = forms.FileField(
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"}),
        required=True
    )

    pledge = forms.FileField(
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"}),
        required=True
    )

    teacher_appreciation = forms.FileField(
        widget=forms.FileInput(attrs={"accept": "image/*,.pdf"}),
        required=True
    )

    class Meta:
        model = Ustaz
        fields = [
            "nid_no",
            "birth_date",
            "birth_certificate_no",
            "nid_front",
            "nid_back",
            "guardian_permission_letter",
            "chairman_certificate",
            "pledge",
            "teacher_appreciation",
        ]
        labels = {
            "nid_no": "National ID Number (if age more than 18 years)",
            "birth_certificate_no": "Birth Certificate Number",
            "nid_front": "NID Front Image (if any)",
            "nid_back": "NID Back Image (if any)",
            "guardian_permission_letter": "Guardian Permission Letter",
            "chairman_certificate": "Chairman Certificate",
            "pledge": "Pledge Document",
            "teacher_appreciation": "Teacher Appreciation Document",
        }

    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get("birth_date")
        nid_no = cleaned_data.get("nid_no")

        if birth_date:
            today = timezone.now().date()
            age = (
                today.year
                - birth_date.year
                - ((today.month, today.day) < (birth_date.month, birth_date.day))
            )

            if age >= 18 and not nid_no:
                raise forms.ValidationError(
                    {
                        "nid_no": "National ID number is required for individuals 18 years or older."
                    }
                )

        return cleaned_data

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(UstazForm, self).__init__(*args, **kwargs)
        if user:
            self.instance.user = user

    @transaction.atomic
    def save(self, user=None, address=None, commit=True):
        ustaz = super().save(commit=False)

        if user:
            ustaz.user = user
        if address:
            ustaz.address = address

        if commit:
            ustaz.save()

        # Handle multiple education files
        education_files = self.files.getlist("education_files")
        for file in education_files:
            EducationalQualification.objects.create(ustaz=ustaz, file=file)

        # Handle multiple training files
        training_files = self.files.getlist("training_files")
        for file in training_files:
            TrainingCertificate.objects.create(ustaz=ustaz, file=file)

        # Handle multiple achievement files
        achievement_files = self.files.getlist("achievement_files")
        for file in achievement_files:
            AchievementCertificate.objects.create(ustaz=ustaz, file=file)

        # Handle multiple testimonial files
        testimonial_files = self.files.getlist("testimonial_files")
        for file in testimonial_files:
            OrganizationTestimonial.objects.create(ustaz=ustaz, file=file)

        return ustaz
