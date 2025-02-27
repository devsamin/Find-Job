from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from job.models import Job
from job_seeker.models import JobSeeker
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from rest_framework.decorators import action
from .models import APPLICATION_STATUS

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = models.Application.objects.all()
    serializer_class = serializer.ApplicationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get_queryset(self):
        queryset = super().get_queryset()
        job_id = self.request.query_params.get('job_id')
        job_seeker_id = self.request.query_params.get('job_seeker_id')

        if job_id:
            queryset = queryset.filter(job_id=job_id)
        if job_seeker_id:
            queryset = queryset.filter(job_seeker_id=job_seeker_id)
        return queryset
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        # print(f"Request User: {request.user}")  # ✅ এখানে লগ দেখবে কে রিকোয়েস্ট করছে
        # print(f"Employer User: {self.get_object().job.employer.user}") 
        """Allow employer to update application status and send email notification"""
            
        try:
            application = self.get_object()

            # ✅ Ensure only the job employer can update the status
            # if request.user != application.job.employer.user:
            #     return Response({"error": "You are not authorized to update this application"}, status=status.HTTP_403_FORBIDDEN)

            new_status = request.data.get("status")
            if new_status not in dict(APPLICATION_STATUS):
                return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

            # ✅ Update application status
            application.status = new_status
            application.save()

            # ✅ Send email notification if status is "Accepted"
            if new_status == "Accepted":
                email_subject = "Congratulations! Your Job Application is Accepted"
                email_body = render_to_string('accepted_application_email.html', {'user': application.job_seeker.user, 'job_title': application.job.title})
                email = EmailMultiAlternatives(email_subject, '', to=[application.job_seeker.user.email])
                email.attach_alternative(email_body, 'text/html')
                email.send()

            return Response({"message": "Status updated successfully and email sent", "status": application.status}, status=status.HTTP_200_OK)

        except models.Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)


# Email sender jonno custom babe abr view make korte holo
class JobApplicationCustomView(APIView):
    def post(self, request, job_id):
        job = models.Job.objects.get(id=job_id)
        job_seeker = JobSeeker.objects.get(user=request.user)

        if not request.user.is_authenticated:
            return Response({'erros': "User must be logged in apply for this job"}, status=status.HTTP_400_BAD_REQUEST)
        # ✅ Check if already applied
        if models.Application.objects.filter(job_id=job_id,job_seeker=job_seeker).exists():
            return Response({'error' : 'You have already applyed this job'}, status=status.HTTP_400_BAD_REQUEST)

        # application make
        job_seeker = JobSeeker.objects.get(user=request.user)

        application = models.Application.objects.create(
            job = job,
            job_seeker = job_seeker,
            resume = request.FILES.get('resume'),
            cover_letter=self.request.data.get('cover_letter')
        )
        # ✅ Send confirmation email
        email_subject = "Job Application Submitted Successfully"
        email_body = render_to_string('confirm_application_email.html', {'user': job_seeker.user, 'job_title': job.title})
        email = EmailMultiAlternatives(email_subject, '', to=[job_seeker.user.email])
        email.attach_alternative(email_body, 'text/html')
        email.send()

        return Response({"message": "Your job application has been submitted successfully. Check your email for confirmation."}, status=status.HTTP_201_CREATED)