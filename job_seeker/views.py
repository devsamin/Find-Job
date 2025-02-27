from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializer
from rest_framework.pagination import PageNumberPagination



class JobseekerPagenation(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class JobSekeerViewset(viewsets.ModelViewSet):
    queryset = models.JobSeeker.objects.all()
    serializer_class = serializer.JobSeekerSerializer
    pagination_class = JobseekerPagenation

