from django.urls import path, include

from . import views

app_name = 'accounts'

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('<int:pk>/activity/', views.user_activity),
]
