from django.urls import path
from blog import views
urlpatterns=[

    path('register/', views.UserRegister,name="register" ),
    path('login/', views.UserLogin, name="login"),
    path('', views.Home, name="home"),
    path('logout/',views.UserLogout,name="logout"),
    path('profile/',views.Profile,name="profile"),
    path('post/',views.PostListView.as_view(),name='post_list'),
    path('post/drafts',views.PostDraftList.as_view(),name='post_draft_list'),
    path('post/<int:pk>',views.PostDetailView.as_view(),name='post_detail'),
    path('post/new',views.CreatePostView.as_view(),name='post_create'),
    path('post/update/<int:pk>',views.PostUpdateView.as_view(),name='post_update'),
    path('post/delete/<int:pk>',views.PostDeleteView.as_view(),name='post_delete'),
    path('post/comment/<int:pk>', views.add_comment_to_post,name='add_comment'),
    path('post/newcomment/<int:pk>', views.add_new__comment_to_post,name='add_new_comment'),
    path('comment/approve/<int:pk>',views.comment_approve,name='comment_approve'),
    path('comment/remove/<int:pk>',views.comment_remove,name='comment_remove'),
    path('post/publish/<int:pk>', views.post_publish, name='post_publish'),
    path('dashboard/', views.Dashboard, name='dashboard'),


]
