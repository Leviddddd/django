from django.contrib import admin, messages
from django.utils.translation import ngettext

from dl.models import *


# Register your models here.


@admin.register(UserVote)
class UserVote(admin.ModelAdmin):
    date_hierarchy = 'create_time'


@admin.register(Vote)
class Vote(admin.ModelAdmin):
    list_display = ('vote_name', 'num', 'force_num', 'status', 'update_time')
    date_hierarchy = 'update_time'
    empty_value_display = '-empty-'
    actions = ['clear_vote_detail']

    def clear_vote_detail(self, request, queryset):
        updated = queryset.update(num=0, force_num=0)
        self.message_user(request, ngettext(
            '%d story was update successfully.',
            '%d stories were update successfully.',
            updated,
        ) % updated, messages.SUCCESS)

    clear_vote_detail.short_description = '清空投票记录'
