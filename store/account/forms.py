from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm as AuthPasswordChangeForm
from django.contrib.auth.models import User

from .models import Profile


class PasswordStrengthValidator():
    min_length = 6

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError('Password must be at least %s characters long.'
                                  % self.min_length, code='password-too-short')

        if value.isdigit() or value.isalpha():
            raise ValidationError('Password must contain both letters and numbers.',
                                  code='password-too-weak')


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].validators.append(PasswordStrengthValidator())

        # Set name and email to be required.
        # http://stackoverflow.com/questions/1134667/django-required-field-in-model-form
        for key in self.fields:
            self.fields[key].required = True

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')

        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set name and email to be required.
        for key in self.fields:
            self.fields[key].required = True


class PasswordChangeForm(AuthPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].validators.append(PasswordStrengthValidator())


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', )