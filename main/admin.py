from django.contrib import admin
from .models import *

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id','user','title')
    list_filter = ('user',)
    search_fields = ('title',)
    list_display_links = ('id','title')
    list_max_show_all=300

admin.site.register(Tag)

    
