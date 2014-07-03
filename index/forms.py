from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from index.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    """
    Extends the built-in Django UserCreationForm, removing username
    and adding email, first name and last name.
    """

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(render_value=True),
        help_text='This password has been randomly generated, only edit this if you want to manually choose a password.')
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput(render_value=True),
        help_text='Enter the same password as above (if changed), for verification.')

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

        # Generate random password, user will be notified with reset email.
        password = CustomUser.objects.make_random_password()
        self.fields['password1'].initial = password
        self.fields['password2'].initial = password

    class Meta:
        model = CustomUser


class CustomUserChangeForm(UserChangeForm):

    """
    Extends the built-in Django UserChangeForm, removing username.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser


class CustomUserUpdateForm(forms.ModelForm):

    """
    Simple front-facing CustomUser form for non-staff use.
    """

    class Meta:
        model = CustomUser
        exclude = ('password', 'last_login', 'groups', 'user_permissions', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
