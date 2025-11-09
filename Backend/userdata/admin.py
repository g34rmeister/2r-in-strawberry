from django.contrib import admin
from .models import *
import nested_admin
from django.contrib.auth import get_user_model
User = get_user_model()

# superuser: william, geaux
admin.site.register(User)
admin.site.register(FriendGroup)
admin.site.register(FriendGroupMembership)

class PlantLibraryEntryInline(nested_admin.NestedStackedInline):
    model = PlantLibraryEntry
    extra = 1 # num of extra forms to show

@admin.register(PlantLibrary)
class RoomAdmin(nested_admin.NestedModelAdmin):
    inlines = [PlantLibraryEntryInline]