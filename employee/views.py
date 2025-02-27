from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializer
from rest_framework.pagination import PageNumberPagination



class EmployeePagenation(PageNumberPagination):
    page_size = 11
    page_size_query_param = 'page_size'
    max_page_size = 100

class EmployeeViewset(viewsets.ModelViewSet):
    queryset = models.Employee.objects.all()
    serializer_class = serializer.EmployeeSerializer
    pagination_class = EmployeePagenation

    

