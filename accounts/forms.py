from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import User, BlogPost
from django.contrib.auth.forms import UserCreationForm
class UserSignupForm(UserCreationForm):
    is_patient = forms.BooleanField(label='Are you a Patient?', required=False)
    is_doctor = forms.BooleanField(label='Are you a Doctor?', required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'profile_picture', 'username', 'email', 'password1', 'password2', 'address_line1', 'city', 'state', 'pincode', 'is_patient', 'is_doctor']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_patient = self.cleaned_data.get('is_patient')
        user.is_doctor = self.cleaned_data.get('is_doctor')
        if commit:
            user.save()
        return user

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        validate_password(password2)  # Validate password strength
        return password2
    
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'image', 'category', 'summary', 'content', 'draft']
