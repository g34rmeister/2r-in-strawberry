from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model
User = get_user_model()

# superuser: william, geaux
admin.site.register(User)
admin.site.register(FriendGroup)
admin.site.register(FriendGroupMembership)
admin.site.register(Card)