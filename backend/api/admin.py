from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Bookmark)
admin.site.register(Notification)