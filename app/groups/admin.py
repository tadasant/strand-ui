from django.contrib import admin

from app.groups.models import Group, GroupSettings

admin.site.register(Group)
admin.site.register(GroupSettings)
