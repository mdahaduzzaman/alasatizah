from django import forms

from core.models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["id"]
        help_texts = {
            "city": "e.g. Dhaka, Khulna, Chittagong",
            "area": "e.g. Dhanmondi, Gulshan, Banani",
            "house": "e.g. House: 67, Road: 15"
        }
