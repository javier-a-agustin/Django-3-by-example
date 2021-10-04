from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('share/<slug>/', views.PostShareView.as_view(), name='post_share'),
]
