from django.contrib import admin

from embed_video.admin import AdminVideoMixin
from . import models

# Register your models here.


class MyModelAdmin(AdminVideoMixin, admin.ModelAdmin):
    pass

admin.site.register(models.videoInfo, MyModelAdmin)

admin.site.register(models.catagory)
admin.site.register(models.videoAndCategory)
admin.site.register(models.comments)