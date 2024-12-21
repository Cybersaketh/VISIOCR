from rest_framework import serializers
from .models import Identity
from django.contrib.auth.models import User


class IdentitySerializer(serializers.ModelSerializer):  # create class to serializer model
    creator = serializers.ReadOnlyField(source='creator.username')
    aadhaar = serializers.CharField(min_length=12, max_length=16)
    pan = serializers.CharField(min_length=10, max_length=10)

    class Meta:
        model = Identity
        fields = ('id', 'name', 'pan', 'aadhaar', 'dob', 'gender','creator')


class UserSerializer(serializers.ModelSerializer):  # create class to serializer user model
    identities = serializers.PrimaryKeyRelatedField(many=True, queryset=Identity.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'identities')
