from django import forms
from .models import User

class UserSignupForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['is_patient','is_doctor','first_name', 'last_name', 'profile_picture', 'username', 'email', 'password', 'password_confirm', 'address_line1', 'city', 'state', 'pincode']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Password and confirm password do not match")
