from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from community_blog import views

urlpatterns=[
	path('index_blog',views.index.as_view(),name='index_blog'),
	path('add_new_blog',views.add_new_blog.as_view(),name='add_new_blog'),
	path('blog_details/<int:user_id>/<int:blog_key>',views.blog_details.as_view(),name='blog_details'),
	path('new_or_existing_user',views.new_or_existing_user.as_view(),name='new_or_existing_user'),
	path('logout_current_session',views.logout_current_session,name='logout_current_session'),
	path('delete_blog/<int:user_id>/<int:blog_id>',views.delete_blog,name='delete_blog'),
	path('edit_blog_items/<int:user_id>/<int:blog_id>',views.edit_blog_items,name='edit_blog_items')
]