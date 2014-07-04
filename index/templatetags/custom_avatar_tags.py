from avatar.util import cache_result, get_primary_avatar
from django import template
from django.conf import settings

register = template.Library()

AVATAR_LOCATION_LIST = (
    'colourworks',
    'fitzroyhouse',
    'printhouse'
)


@cache_result()
@register.simple_tag
def avatar_url(user, size=settings.AVATAR_DEFAULT_SIZE):
    avatar = get_primary_avatar(user, size=size)

    if avatar:
        return avatar.avatar_url(size)

    base_url = getattr(settings, 'STATIC_URL', None)
    if not base_url:
        base_url = getattr(settings, 'MEDIA_URL', '')

    image_url = 'images/tenants.jpg'

    if user.location:
        building = ''.join(user.location.building.split(' ')).lower()
        if building in AVATAR_LOCATION_LIST:
            image_url = 'images/%s.jpg' % building

    return '%s%s' % (base_url, image_url)
