from django.contrib.auth.models import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    """ Mostly duplicates built-in Django UserManager, handling index.CustomUser requirements. """

    def _create_user(self, email, first_name, last_name, password, is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email, first name, last name and password.
        """
        now = timezone.now()

        if not email:
            raise ValueError('The given email must be set')
        if not first_name:
            raise ValueError('The given first name must be set')
        if not last_name:
            raise ValueError('The given last name must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name,
                          is_staff=is_staff, is_active=True, is_superuser=is_superuser,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, first_name, last_name, password=None, **extra_fields):
        """
        Creates User without staff permissions.
        """
        return self._create_user(email, first_name, last_name, password, False, False, **extra_fields)

    def create_superuser(self, email, first_name, last_name, password, **extra_fields):
        """
        Creates User with superuser (and staff) permissions.
        """
        return self._create_user(email, first_name, last_name, password, True, True, **extra_fields)

    def public(self):
        """
        Filters Users displayed publically in index.
        """
        return self.get_queryset().filter(in_tenant_index=True)

    def staff(self):
        """
        Filters Users displayed publically in index.
        """
        return self.get_queryset().filter(in_staff_index=True)
