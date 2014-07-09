from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from index.models import CustomUser
from index.widgets import DayMonthWidget


class MessageForm(forms.Form):

    """
    Simple form used to send email messages.
    """

    recipient = forms.IntegerField(widget=forms.HiddenInput, required=False)
    subject = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)


class CustomUserCreationForm(UserCreationForm):

    """
    Extends the built-in Django UserCreationForm, removing username
    and adding email, first name and last name.
    """

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

    """
    Extends the built-in Django UserChangeForm, removing username.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        widgets = {
            'birthday': DayMonthWidget
        }



class CustomUserUpdateForm(forms.ModelForm):

    """
    Simple front-facing CustomUser form for non-staff use.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserUpdateForm, self).__init__(*args, **kargs)

        # Update description for (non-staff) users
        self.fields['is_in_index'].label = 'Show me in the tenant index'
        self.fields['is_in_index'].help_text = ('Deselect to remove yourself '
            'from the list. You\'ll always be able to use this site and browse '
            'the list regardless. <br/> Note that only logged users authorised by '
            'Bootstrap will ever be able to see the list anyway.')

    class Meta:
        model = CustomUser

        exclude = ('password', 'last_login', 'groups', 'user_permissions', 'date_joined', 'is_active', 'is_staff', 'is_superuser')
        widgets = {
            'birthday': DayMonthWidget
        }
