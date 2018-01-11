from django.contrib import admin

from app.slack.models import SlackChannel, SlackSettings, SlackTeam, SlackUser

admin.site.register(SlackTeam)
admin.site.register(SlackSettings)
admin.site.register(SlackUser)
admin.site.register(SlackChannel)