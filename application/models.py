from django.db import models
from job.models import Job
from job_seeker.models import JobSeeker

APPLICATION_STATUS = [
    ('Applied', 'Applied'),
    ('Accepted', 'Accepted'),
]


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="applications")
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name="applications")
    resume = models.FileField(upload_to="application/applications", null=True, blank=True)
    cover_letter = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=40, choices=APPLICATION_STATUS, default='Applied')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.job_seeker} applied for {self.job.title}"

