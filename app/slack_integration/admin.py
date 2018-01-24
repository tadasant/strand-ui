from django.contrib import admin

from app.slack_integration.models import SlackChannel, SlackTeam, SlackTeamInstallation, SlackUser


class SlackChannelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slack_team')


class SlackUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'real_name', 'display_name', 'slack_team')


admin.site.register(SlackChannel, admin_class=SlackChannelAdmin)
admin.site.register(SlackTeam)
admin.site.register(SlackTeamInstallation)
admin.site.register(SlackUser, admin_class=SlackUserAdmin)
