from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from index.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):

    """ Mostly duplicates built-in Django User model, with required unique email as username field,
    removing username actual, also requiring first_name and last_name. """

    # Authentication and control
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))

    # Additional information
    industries = models.ManyToManyField('Industry', null=True, blank=True)
    location = models.ForeignKey('Location', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class Industry(models.Model):

    """ Simple representation of an Industry, related M2M of index.CustomUser. """

    name = models.CharField(_('name'), max_length=50, unique=True)

    class Meta:
        verbose_name_plural = _('industries')

    def __unicode__(self):
        return self.name


class Location(models.Model):

    """ Simple representation of a Location, related FK of index.CustomUser. """

    building = models.CharField(_('building'), max_length=50)
    floor = models.IntegerField(_('floor'), default=0, help_text=_('Use zero for ground floor.'))

    def floor_readable(self):
        if self.floor > 0:
            nth = {
                1: "st",
                2: "nd",
                3: "rd"
            }
            return '%s%s floor' % (self.floor, nth.get(self.floor, 'th'))
        else:
            return 'Ground floor'

    def __unicode__(self):
        return self.floor_readable() + ', ' + self.building
