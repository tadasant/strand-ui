from django.contrib import admin

from app.slack_integration.models import SlackChannel, SlackTeam, SlackTeamInstallation, SlackUser

admin.site.register(SlackTeam)
admin.site.register(SlackTeamInstallation)
admin.site.register(SlackUser)
admin.site.register(SlackChannel)
