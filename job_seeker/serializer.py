from rest_framework import serializers
from django.contrib.auth.models import User
from . import models
from employee.models import Employee

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']  #


class JobSeekerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = models.JobSeeker
        # fields = '__all__'
        fields = ['id', 'user', 'resume', 'skills', 'location', 'profile_image','mobile_no']

