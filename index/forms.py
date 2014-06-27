from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from index.models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    """
    Extends the built-in Django UserCreationForm, removing username
    and adding email, first name and last name.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name')


class CustomUserChangeForm(UserChangeForm):

    """
    Extends the built-in Django UserChangeForm, removing username.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
