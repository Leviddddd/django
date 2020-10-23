from django.test import TestCase

# Create your tests here.
from dl import models

local_user = models.AuthUser.objects.filter().values('username')
user_list = []
for i in local_user:
    user_list.append(i)
print(user_list)