from django.shortcuts import render

from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from .models import Identity
from .permissions import IsOwnerOrReadOnly
from .serializers import IdentitySerializer
from .pagination import CustomPagination
from .filters import IdentityFilter




class ListCreateIdentityAPIView(ListCreateAPIView):
    serializer_class = IdentitySerializer
    queryset = Identity.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IdentityFilter

    def perform_create(self, serializer):
        # Assign the user who created the identity
        serializer.save(creator=self.request.user)


class RetrieveUpdateDestroyIdentityAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = IdentitySerializer
    queryset = Identity.objects.all()
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


