from django.contrib import admin

from app.messages.models import Message, Reply

admin.site.register(Message)
admin.site.register(Reply)
