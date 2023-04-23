from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.post_creation),
    path('<int:pk>/media/add/', views.media_creation),
    path('<int:pk>/likes/add/', views.post_like_creation),
]
