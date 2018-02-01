from django.contrib import admin

from app.dialogues.models import Message, Reply


class MessageAdmin(admin.ModelAdmin):
    list_display = ('time', 'author', 'session')


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('time', 'author', 'message')


admin.site.register(Message, admin_class=MessageAdmin)
admin.site.register(Reply, admin_class=ReplyAdmin)
