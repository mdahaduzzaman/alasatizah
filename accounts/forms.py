from django import forms
from accounts.choices import GenderChoices
from accounts.models import User


class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus repeated password on the admin panel
    """
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            "email",
            "name",
            "phone",
            "gender",
            "avatar",
            "roles",
            "user_permissions",
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            self.save_m2m()
        return user


class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=GenderChoices.choices, widget=forms.Select)
    phone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "inputmode": "numeric",
                "pattern": "[0-9]*",
                "oninput": "this.value = this.value.replace(/[^0-9]/g, '')",
            }
        )
    )

    class Meta:
        model = User
        fields = ["name", "email", "phone", "avatar", "gender"]

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match")
        return cleaned_data


class SignInForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
            }
        )
    )
    remember_me = forms.BooleanField(required=False)


class ProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=GenderChoices.choices, widget=forms.Select)

    class Meta:
        model = User
        fields = ["name", "phone", "gender", "avatar"]
        widgets = {
            "avatar": forms.FileInput(
                attrs={
                    "class": "block w-full border px-3 py-1 rounded-md",
                }
            ),
        }
