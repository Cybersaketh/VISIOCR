from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListCreateIdentityAPIView.as_view(), name='get_post_identities'),
    path('<int:pk>/', views.RetrieveUpdateDestroyIdentityAPIView.as_view(), name='get_delete_update_identities'),
]