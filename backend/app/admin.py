from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *

admin.site.register(User, UserAdmin)
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(FriendRequest)
admin.site.register(Comment)
admin.site.register(Like)
