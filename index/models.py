from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Tenant(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    bio = models.CharField(null=True, blank=True,max_length=255)
    company = models.CharField(max_length=50, null=True, blank=True)
    moved_in_date = models.DateTimeField(verbose_name='date moved in', null=True, blank=True)

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Tenant.objects.create(user_id=instance.id)

post_save.connect(create_user_profile, sender=User)
