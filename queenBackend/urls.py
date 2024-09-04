import os
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include

from queenBackend import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mypp.urls')),
    path('queen/', include('tapp.urls')),
]
