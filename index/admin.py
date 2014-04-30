from django.contrib import admin
from index.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    """ Admin class for UserProfile. """
    list_display = ('user', 'user_first_name', 'user_last_name', 'company')

    def user_first_name(self, obj):
            return obj.user.first_name

    user_first_name.short_description = 'First name'

    def user_last_name(self, obj):
            return obj.user.last_name

    user_last_name.short_description = 'Last name'


admin.site.register(UserProfile, UserProfileAdmin)
