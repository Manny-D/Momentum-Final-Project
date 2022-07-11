from django.contrib import admin
from .models import User, Note, RecipeVersion, TasterFeedback

admin.site.register(User)
admin.site.register(Note)
admin.site.register(TasterFeedback)

# For Taggit admin view
@admin.register(RecipeVersion)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'chef', 'tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
