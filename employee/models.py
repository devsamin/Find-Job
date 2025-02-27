from django.db import models
from django.contrib.auth.models import User

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    company_name = models.CharField(max_length=30)
    company_description = models.TextField()
    logo = models.ImageField(upload_to='employee/company_logo/', null=True, blank=True)
    profile_image = models.ImageField(upload_to='employee/porfile_images/', null=True, blank=True)

    def __str__(self):
        return self.company_name
    

