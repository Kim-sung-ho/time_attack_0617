from django.contrib import admin
from user.models import User, UserProfile, Hobby
# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Hobby)
