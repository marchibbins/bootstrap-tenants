from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.sites.models import Site
from django.core import signing
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.template import loader
from django.utils import timezone
from index.managers import CustomUserManager
from password_reset.forms import PasswordRecoveryForm
from password_reset.views import SaltMixin


class CustomUser(AbstractBaseUser, PermissionsMixin):

    """ Mostly duplicates built-in Django User model, with required unique email as username field,
    removing username actual, also requiring first_name and last_name. """

    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30)
    last_name = models.CharField('last name', max_length=30)
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    is_staff = models.BooleanField('staff status', default=False,
        help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True,
        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    is_in_index = models.BooleanField('displayed in index', default=True,
        help_text='Designates whether this user should be shown in the tenant index list. Unselect this to remove users from index list.')

    bio = models.TextField('bio', null=True, blank=True)
    website = models.URLField('website', null=True, blank=True)
    company = models.CharField('company', max_length=50, null=True, blank=True)
    date_moved_in = models.DateField('date moved in', null=True, blank=True)
    industries = models.ManyToManyField('Industry', null=True, blank=True)
    location = models.ForeignKey('Location', null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

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

    def email_user(self, subject, message, from_email=settings.DEFAULT_FROM_EMAIL):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


@receiver(models.signals.post_save, sender=CustomUser, dispatch_uid="customuser_created")
def notify_created_user(sender, instance, created, **kwargs):
    """
    Send an email to the new User to set their own password.
    """
    if created:
        user = instance
        form = PasswordRecoveryForm(data={'username_or_email': user.email})
        if form.is_valid():
            context = {
                'user': user,
                'username': user.email,
                'secure': settings.SITE_SECURE,
                'site': Site.objects.get_current(),
                'token': signing.dumps(user.pk, salt=SaltMixin.salt),
            }
            body = loader.render_to_string('auth/new_email.txt', context).strip()
            subject = loader.render_to_string('auth/new_email_subject.txt', context).strip()
            user.email_user(subject, body)


class Industry(models.Model):

    """ Simple representation of an Industry, related M2M of index.CustomUser. """

    name = models.CharField('name', max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'industries'

    def __unicode__(self):
        return self.name


class Location(models.Model):

    """ Simple representation of a Location, related FK of index.CustomUser. """

    building = models.CharField('building', max_length=50)
    floor = models.IntegerField('floor', default=0, help_text='Use zero for ground floor.')

    def floor_readable(self):
        """
        Returns readable floor description from integer.
        """
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
