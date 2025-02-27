from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializer.CategorySerializer
