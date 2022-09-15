from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate

urlpatterns = [
    path('posts/', PostList.as_view(), name='home'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('update/<int:pk/', PostUpdate.as_view(), name='post_update'),
    ]