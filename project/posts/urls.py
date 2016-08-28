from django.conf.urls import url
from . import  views

urlpatterns = [
    url(r'create', views.posts_create, name='create' ),
    url(r'update/(?P<slug>[\w-]+)', views.posts_update, name='update' ),
    url(r'detail/(?P<slug>[\w-]+)', views.posts_detail, name='detail' ),
    url(r'delete/(?P<slug>[\w-]+)', views.posts_delete, name='delete' ),
    url(r'list',  views.posts_list, name='list' ),
    url(r'^$',  views.posts_list, name='list' ),
]

