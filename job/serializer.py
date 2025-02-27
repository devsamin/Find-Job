from rest_framework import serializers
from . import models
from employee.serializer import EmployeeSerializer
from category.serializer import CategorySerializer
from category.models import Category
from employee.models import Employee
from .models import BlogPost


class JobSerializer(serializers.ModelSerializer):
    # employer = serializers.StringRelatedField(many=False)
    employer = EmployeeSerializer(read_only=True)
    # category = CategorySerializer()
    # employer = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())  # Ensure it is a valid Employee ID
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all()) 
    class Meta:
        model = models.Job
        fields = ['id', 'title', 'description', 'requirement', 'location', 'salary', 'posted_on', 'employer', 'category', 'job_type']
        
        
    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance



class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
