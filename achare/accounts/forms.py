from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from phonenumber_field.formfields import PhoneNumberField


User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    phone_number = PhoneNumberField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields=["phone_number"]


    def clean_password2(self):
        data = self.cleaned_data
        password1 = data['password1']
        password2 = data['password2']
        if not (password1 and password2):
            raise forms.ValidationError('please fill the password 1 or 2 ..!!!')
        if data['password2'] != data['password2']:
            raise forms.ValidationError('second passworrd is wrong ..!!! **')
        
        return data['password2']

    def save(self, commit=True):
        
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password2"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ['phone_number', 'password', 'is_active', 'is_admin']

    def clean_password(self):
        
        return self.initial["password"]

