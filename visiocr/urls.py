
from django.contrib import admin
from django.urls import include, path

# urls
urlpatterns = [
    path('api/v1/identities/', include('identities.urls')),
    path('api/v1/auth/', include('authentication.urls')),
    path('admin/', admin.site.urls),
    path('file_app/', include('file_app.urls')), 
    path('', include('images.urls')),  # Include images app URLs


]

