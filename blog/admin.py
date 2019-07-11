from django.contrib import admin
from . models import Post,Comment
# Register your models here.
#admin.site.register(Post)
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author','status','publish','created')
    list_filter = ('publish','author','status')
    search_fields = ('status','title')
    prepopulated_fields = {'slug':('title',)}
    #prepopulated_fields is an dictionary
    date_hierarchy = 'publish'
    raw_id_fields = ('author',)
    #ordering = ('-publish',)
    ordering = ('status','publish')

admin.site.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name','email','post','created','active')
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')