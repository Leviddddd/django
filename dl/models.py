# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.


from django.db import models


# Unable to inspect table 'table'
# The error was: (1146, "Table 'LWH.table' doesn't exist")
from django.utils.datetime_safe import datetime


class AuthUser(models.Model):
    id = models.AutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'

    def __str__(self):
        return self.id


class Vote(models.Model):
    vote_name = models.CharField(max_length=255, blank=True, null=True)
    num = models.IntegerField()
    force_num = models.IntegerField()
    create_time = models.DateTimeField(default=datetime.now)
    update_time = models.DateTimeField(default=datetime.now)

    class Meta:
        managed = False
        db_table = 'vote'


class UserVote(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    vote_id = models.IntegerField()
    vote_type = models.IntegerField()
    create_time = models.DateTimeField(blank=True, null=True, default=datetime.now)
    update_time = models.DateTimeField(blank=True, null=True, default=datetime.now)

    class Meta:
        managed = False
        db_table = 'user_vote'
