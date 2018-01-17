from django.contrib import admin

from app.slack.models import SlackChannel, SlackTeam, SlackTeamInstallation, SlackTeamSetting, SlackUser

admin.site.register(SlackTeam)
admin.site.register(SlackTeamInstallation)
admin.site.register(SlackTeamSetting)
admin.site.register(SlackUser)
admin.site.register(SlackChannel)
