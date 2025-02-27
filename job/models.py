from django.db import models
from employee.models import Employee
from category.models import Category

JOB_TYPES = [
    ('FullTime', 'FullTime'),
    ('PartTime', 'PartTime'),
    ('Internship', 'Internship')
]

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirement = models.CharField(max_length=250)
    location = models.CharField(max_length=200)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True) 
    posted_on = models.DateTimeField(auto_now_add=True)
    employer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="jobs")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="jobs")

    # add new field
    job_type = models.CharField(choices=JOB_TYPES, default='PartTime', max_length=20, blank=True, null=True)

    def __str__(self):
        return self.title

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to="blog_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title