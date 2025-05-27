from django import forms

from posts.models import JobPost, UstazJobRequest


class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            "title",
            "description",
            "salary",
            "job_time",
            "job_type",
            "tuition_time",
            "deadline",
            "subjects",
            "ustaz_type",
            "status",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }


class UstazJobRequestForm(forms.ModelForm):
    class Meta:
        model = UstazJobRequest
        fields = [
            "title",
            "bio",
            "subjects",
            "classes",
            "job_time",
            "job_type",
            "tuition_time",
            "expected_salary",
            "status",
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4})
        }
        help_texts = {
            "expected_salary": "Leave blank if negotiable.",
        }

