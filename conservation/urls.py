from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('evidence/', include('evidence.urls')),
    path('admin/', admin.site.urls),
]
