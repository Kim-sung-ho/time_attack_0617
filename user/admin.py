from django.contrib import admin
from user.models import User as UserModel
from user.models import UserProfile as UserProfileModel
from user.models import Hobby as HobbyModel
from user.models import UserType as UserTypeModel
from user.models import UserLog as UserLogModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(UserProfileModel)
admin.site.register(HobbyModel)
admin.site.register(UserTypeModel)
admin.site.register(UserLogModel)
