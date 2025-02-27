from django.db import models
from django.contrib.auth.models import User


class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="job_seeker")
    resume = models.FileField(upload_to='job_seeker/resumes/', null=True, blank=True)
    skills = models.TextField()
    location = models.CharField(max_length=233)
    mobile_no = models.CharField(max_length=13, blank=True, null=True)
    profile_image = models.ImageField(upload_to='job_seeker/profile_images/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
