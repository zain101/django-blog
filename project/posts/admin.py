from django.contrib import admin
from .models import Post

# Register your models here.
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'title', 'timestamp','updated', )
    list_display_links = ('updated', )
    list_filter = ('updated', )
    search_fields = ('title', 'content' )
    list_editable = ('title', )
    class Meta:
        model = Post



admin.site.register(Post, PostModelAdmin)