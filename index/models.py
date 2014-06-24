from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save

import logging
from inspector_panel import debug

class Industry(models.Model):
    name = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    building = models.CharField(max_length=50)
    floor = models.IntegerField(default=0)

    def get_floor_suffix(self, floor):
        nth = {
            1: "st",
            2: "nd",
            3: "rd"
        }
        return nth.get(floor%10, 'th');

    def floor_human_readable(self):
        floor_suffixed = ''
        if self.floor > 0:
            floor_suffixed = ''.join([str(self.floor), self.get_floor_suffix(self.floor)])
        else:
            floor_suffixed = 'Ground'
        return floor_suffixed + ' floor'

    def __unicode__(self):
        return self.floor_human_readable() + ', ' + self.building


class Tenant(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    bio = models.CharField(null=True, blank=True,max_length=255)
    company = models.CharField(max_length=50, null=True, blank=True)
    moved_in_date = models.DateTimeField(verbose_name='date moved in',
                                         null=True, blank=True)
    industries = models.ManyToManyField(Industry, null=True, blank=True)
    location = models.ForeignKey(Location, null=True, blank=True)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Tenant.objects.create(user=instance)

def create_user(sender, **kwargs):
    # user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    logging.debug(type(kwargs['instance']))
    logging.debug(kwargs['instance'])
    debug([1,2,3])
    # if True:
    #     Tenant.objects.create(user=instance)

pre_save.connect(create_user, sender=Tenant)
