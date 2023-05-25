from django.contrib import admin
from .models import FriendRequest

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'fromUser', 'toUser', 'status', 'created', 'updated', 'group')
    readonly_fields = ('created', 'updated')


admin.site.register(FriendRequest, FriendRequestAdmin)
