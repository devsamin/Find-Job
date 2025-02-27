from django.shortcuts import render
from rest_framework import viewsets
from django.db.models import Q
from . import models
from . import serializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import ValidationError
from employee.models import Employee

class JobPagenation(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100




class JobViewset(viewsets.ModelViewSet):
    queryset = models.Job.objects.all()
    serializer_class = serializer.JobSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]
    pagination_class = JobPagenation

    # employee tar nije post kora job gula filter korte parbe ?employee_id = (id)
    def get_queryset(self):
        queryset = super().get_queryset() # sob object k anlam
        employer_id = self.request.query_params.get('employer_id')
        category_name = self.request.query_params.get('category_name')
        location = self.request.query_params.get('location')
        keyword = self.request.query_params.get('keyword')

        if employer_id:
            queryset = queryset.filter(employer_id = employer_id)
        if category_name:
            queryset = queryset.filter(category__name__icontains=category_name) 
        if location:
            queryset = queryset.filter(location__iexact=location)
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | 
                Q(description__icontains=keyword) | 
                Q(requirement__icontains=keyword)
            )
        if not queryset.exists():
            raise NotFound(detail="No jobs found matching your criteria")
        return queryset
    

class Jobpostviews(APIView):
    def post(self, request, *args, **kwargs):
        serializers = serializer.JobSerializer(data = request.data)
        # print(serializers)
        if serializers.is_valid():
            user = request.user
            print("employee",user)
            try:
                employee = Employee.objects.get(user = user)
            except models.Employee.DoesNotExist:
                return Response(
                    {"error": "Employee not found for the logged-in user."},
                    status=status.HTTP_404_NOT_FOUND
                )
            serializers.save(employer=employee)
            return Response(serializers.data, status=status.HTTP_201_CREATED)

        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    

class JobDetailAPIView(APIView):
    def get(self, request, pk):
        job = get_object_or_404(models.Job, pk=pk)
        serializers = serializer.JobSerializer(job)
        # print("Job Data:", serializers.data)  # Debugging
        return Response(serializers.data, status=status.HTTP_200_OK)
    
class BlogPostViewset(viewsets.ModelViewSet):
    queryset = models.BlogPost.objects.all()
    serializer_class = serializer.BlogPostSerializer

