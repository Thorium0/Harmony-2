from django.contrib import admin

from .models import Message

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'sender', 'content', 'created', 'updated', 'image')
    readonly_fields = ('created', 'updated')

admin.site.register(Message, CommentAdmin)