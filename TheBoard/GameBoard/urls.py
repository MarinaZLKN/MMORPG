from django.urls import path

from .views import PostList, PostDetail, PostCreate, PostUpdate, IndexView, MainPage, Comments, DeleteComment, approve,\
    disapprove

urlpatterns = [
    path('posts/', PostList.as_view(), name='home'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('update/<int:pk/', PostUpdate.as_view(), name='post_update'),
    path('mypage/', IndexView.as_view(), name='mypage'),
    path('', MainPage.as_view(), name='main'),
    path('<int:pk>/add_comment/', Comments.as_view(), name='add_comment'),
    path('delete/<int:pk>/', DeleteComment.as_view(), name='delete_comment'),
    path('approve/<int:pk>/', approve, name='approve'),
    path('disapprove/<int:pk>/', disapprove, name='disapprove'),

    ]
