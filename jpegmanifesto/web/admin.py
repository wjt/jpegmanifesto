from django.contrib import admin
from .models import UploadedImage, MangledImage

class MangledInline(admin.StackedInline):
    model = MangledImage
    extra = 0


class UploadedImageAdmin(admin.ModelAdmin):
    inlines = [MangledInline]

admin.site.register(UploadedImage, UploadedImageAdmin)
