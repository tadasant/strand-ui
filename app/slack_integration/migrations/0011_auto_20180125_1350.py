# Generated by Django 2.0.1 on 2018-01-25 13:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('slack_integration', '0010_slackteaminstallation_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slackchannel',
            name='slack_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slack_channels', to='slack_integration.SlackTeam'),
        ),
        migrations.AlterField(
            model_name='slackteaminstallation',
            name='slack_team',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='slack_integration.SlackTeam'),
        ),
        migrations.AlterField(
            model_name='slackuser',
            name='slack_team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slack_users', to='slack_integration.SlackTeam'),
        ),
        migrations.AlterField(
            model_name='slackuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slack_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
