from django.contrib import admin

# Register your models here.
from .models import User, DirectoryUser, FileUser

admin.site.register(User)
admin.site.register(DirectoryUser)
admin.site.register(FileUser)
