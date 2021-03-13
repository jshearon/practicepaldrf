# Generated by Django 3.1.3 on 2021-03-12 14:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AppUsers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='userimages/None/no-img.jpg', upload_to='userimages/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Instruments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Songs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('composer', models.CharField(max_length=250)),
                ('pdf', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('instrument', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instruments', related_query_name='instrument', to='practicepalapi.instruments')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs_appusers', related_query_name='songs_appuser', to='practicepalapi.appusers')),
            ],
        ),
        migrations.CreateModel(
            name='Sections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=50)),
                ('initial_bpm', models.IntegerField()),
                ('target_bpm', models.IntegerField()),
                ('is_complete', models.BooleanField(default=False)),
                ('pdf_page_nums', models.JSONField()),
                ('beats', models.IntegerField(default=4)),
                ('division', models.IntegerField(default=4)),
                ('tries', models.IntegerField(default=3)),
                ('section_users', models.ManyToManyField(related_name='section_users', related_query_name='sections_user', to='practicepalapi.AppUsers')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='practicepalapi.songs')),
            ],
        ),
        migrations.CreateModel(
            name='Competitions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition_creators', related_query_name='competition_creator', to='practicepalapi.appusers')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='competition_sections', related_query_name='competition_section', to='practicepalapi.sections')),
            ],
        ),
        migrations.CreateModel(
            name='Attempts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bpm', models.IntegerField()),
                ('success', models.BooleanField()),
                ('attempted_on', models.DateTimeField(auto_now_add=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_attempts', related_query_name='section_attempt', to='practicepalapi.sections')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_attempts', related_query_name='user_attempt', to='practicepalapi.appusers')),
            ],
        ),
    ]
