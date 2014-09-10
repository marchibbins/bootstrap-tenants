from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm, ERROR_MESSAGE
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from index.models import CustomUser
from index.widgets import DayMonthWidget


class MessageForm(forms.Form):

    """ Simple form used to send email messages. """

    recipient = forms.IntegerField(widget=forms.HiddenInput, required=False)
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class CustomAdminAuthenticationForm(AdminAuthenticationForm):

    """ Overrides built-in form to allow non-staff superuser access. """

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE
        params = {'username': self.username_field.verbose_name}

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(message, code='invalid', params=params)
            elif not self.user_cache.is_active or not (self.user_cache.is_staff or self.user_cache.is_superuser):
                raise forms.ValidationError(message, code='invalid', params=params)
        return self.cleaned_data


class CustomUserCreationForm(UserCreationForm):

    """ Extends the built-in Django UserCreationForm, removing username
    and adding email, first name and last name. """

    password1 = forms.CharField(widget=forms.HiddenInput)
    password2 = forms.CharField(widget=forms.HiddenInput)

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

        # Generate random password, user will be notified with reset email.
        password = CustomUser.objects.make_random_password()
        self.fields['password1'].initial = password
        self.fields['password2'].initial = password

    class Meta:
        model = CustomUser
        widgets = {
            'birthday': DayMonthWidget
        }


class CustomUserChangeForm(UserChangeForm):

    """ Extends the built-in Django UserChangeForm, removing username. """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        widgets = {
            'birthday': DayMonthWidget
        }


class CustomUserUpdateForm(forms.ModelForm):

    """ Simple front-facing CustomUser form for non-staff use. """

    def __init__(self, *args, **kargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kargs)

        # Update description for (non-staff) users
        self.fields['in_tenant_index'].label = 'Show me in the tenant index'
        self.fields['in_tenant_index'].help_text = ('Deselect to remove yourself '
            'from the tenant list. You\'ll always be able to use this site and browse '
            'the list regardless. <br/> Note that only logged users authorised by '
            'Bootstrap will ever be able to see the list anyway.')

        # Handle staff fields conditionally
        if kargs['instance'].in_staff_index:
            self.fields['in_staff_index'].label = 'Show me in the staff index'
            self.fields['in_staff_index'].help_text = ('Deselect to remove yourself '
                'from the staff list. If you change your mind later, you\'ll need '
                'an admin to add you again.')
            self.fields['staff_role'].help_text = ('What is your role, title, or responsibilities?')
        else:
            del self.fields['staff_role']
            del self.fields['in_staff_index']

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'website', 'company',
            'industries', 'location', 'additional_location', 'birthday',
            'staff_role', 'in_staff_index', 'in_tenant_index')
        widgets = {
            'birthday': DayMonthWidget,
            'industries': forms.CheckboxSelectMultiple(),
        }
