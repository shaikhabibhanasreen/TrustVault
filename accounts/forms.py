from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

        email = forms.EmailField(required=True)

def save(self, commit=True):
    user = super().save(commit=False)
    user.email = self.cleaned_data["email"]

    if commit:
        user.save()

    return user
