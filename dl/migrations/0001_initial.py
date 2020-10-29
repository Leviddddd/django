# Generated by Django 3.1.2 on 2020-10-29 15:09

from django.db import migrations, models
import django.utils.datetime_safe


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UserVote',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('vote_id', models.IntegerField()),
                ('vote_type', models.IntegerField()),
                ('status', models.IntegerField(null=True)),
                ('create_time', models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now, null=True)),
                ('update_time', models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now, null=True)),
            ],
            options={
                'db_table': 'user_vote',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote_name', models.CharField(blank=True, max_length=255, null=True)),
                ('num', models.IntegerField()),
                ('force_num', models.IntegerField()),
                ('status', models.IntegerField(blank=True, null=True)),
                ('create_time', models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now, null=True)),
                ('update_time', models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now, null=True)),
            ],
            options={
                'db_table': 'vote',
                'managed': False,
            },
        ),
    ]
