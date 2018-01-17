from django.contrib import admin

from app.groups.models import Group, GroupSetting

admin.site.register(Group)
admin.site.register(GroupSetting)
