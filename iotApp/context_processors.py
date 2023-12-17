from iotAppMidproject import settings


def username(request):
    username = request.user.username if request.user.is_authenticated else None

    return {
        'username': username,
        'MEDIA_URL' : settings.MEDIA_URL
    }