from django.contrib import admin
from community_blog.models import NewBlog,create_new_user
# Register your models here.
admin.site.register(NewBlog)
admin.site.register(create_new_user)