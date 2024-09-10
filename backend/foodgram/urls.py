from django.contrib import admin
from django.urls import path, include

from api.urls import urls as api_urls
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('api-token-auth/', obtain_auth_token),
]
