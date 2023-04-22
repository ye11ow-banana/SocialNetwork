from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/accounts/', include('accounts.urls')),
    path('api/posts/', include('posts.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
