# Generated by Django 3.1.3 on 2021-03-29 05:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('practicepalapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitee_appusers', related_query_name='invitee_appuser', to='practicepalapi.appusers')),
                ('inviter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inviter_appusers', related_query_name='inviter_appuser', to='practicepalapi.appusers')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invite_sections', related_query_name='invite_section', to='practicepalapi.sections')),
            ],
        ),
    ]
