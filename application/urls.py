from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register('list', views.ApplicationViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('apply/job/<int:job_id>/', views.JobApplicationCustomView.as_view(), name="apply_job"),

    
    
    # API for updating application status
    path('update-status/<int:pk>/', views.ApplicationViewSet.as_view({'patch': 'update_status'}), name="update_application_status"),
]
