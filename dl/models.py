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


class UserVote(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='用户Id')
    vote_id = models.IntegerField(verbose_name='投票id')
    vote_type = models.IntegerField(verbose_name='投票类型')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    class Meta:
        ordering = ['-update_time']
        managed = False
        db_table = 'user_vote'
        verbose_name = u'用户投票记录'
        unique_together = ('user_id', 'vote_type')


class Vote(models.Model):
    vote_name = models.CharField(max_length=255, blank=True, null=True, verbose_name='开会时间')
    num = models.IntegerField(verbose_name='投票数')
    force_num = models.IntegerField(verbose_name='强制投票数')
    status = models.IntegerField(blank=True, null=True, verbose_name='是否开会')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['pk']
        verbose_name = '投票记录'
        managed = False
        db_table = 'vote'


class Meeting(models.Model):
    meet_name = models.CharField(max_length=200, null=True, verbose_name='开会时间')
    vote_list = models.CharField(max_length=255, null=True, verbose_name='投票记录列表')
    meeting_date = models.CharField(max_length=50, null=True, verbose_name='开会周期')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ['pk']
        verbose_name = '开会记录'
        managed = False
        db_table = 'meeting'

    def __str__(self):
        return self.meet_name


STATUS_CHOICES = [
    (0, '未开会'),
    (1, '开会')
]