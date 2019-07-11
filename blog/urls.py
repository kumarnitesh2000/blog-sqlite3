from django.urls import path,include
from . import views
app_name = 'blog'
urlpatterns = [
    path('',views.post_list,name="post_list"),
    path('test/',views.filter,name="test"),
    #tag/django/
    path('tag/<slug:tag_slug>/',views.post_list,name="post_list_by_tag"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name="post_detail"),
    path('<int:post_id>/share/',views.post_share,name="post_share")
]