from django.contrib import admin
from . import models

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'posted_on', 'employer', 'category']
    search_fields = ['title', 'location']
    list_filter = ['category', 'posted_on']

admin.site.register(models.Job, JobAdmin)

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('created_at',)
admin.site.register(models.BlogPost, BlogPostAdmin)