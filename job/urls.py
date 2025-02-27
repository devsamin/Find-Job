from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register('list', views.JobViewset)
router.register('blog', views.BlogPostViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('jobpost/', views.Jobpostviews.as_view(), name='jobpost'),
    path('details/<int:pk>/', views.JobDetailAPIView.as_view(), name="details")
]