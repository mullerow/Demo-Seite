from django.contrib import admin
from .models import CustomUser,UserImageModel, IndexCommentModel, PostModel, VisitorCountModel

class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(CustomUser)
admin.site.register(UserImageModel)
admin.site.register(IndexCommentModel)
admin.site.register(PostModel)
admin.site.register(VisitorCountModel)
