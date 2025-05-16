from django import forms

from core.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["id"]
