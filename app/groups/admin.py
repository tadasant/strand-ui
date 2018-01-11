from django.contrib import admin

from app.slack.models import Group, GroupSettings

admin.site.register(Group)
admin.site.register(GroupSettings)
