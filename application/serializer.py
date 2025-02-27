from rest_framework import serializers
from . import models
from job_seeker.serializer import JobSeekerSerializer
from job.serializer import JobSerializer
class ApplicationSerializer(serializers.ModelSerializer):
    # job_seeker = serializers.StringRelatedField(many=False)
    job_seeker = JobSeekerSerializer(read_only=True)
    job = JobSerializer(read_only=True)

    class Meta:
        model = models.Application
        fields = '__all__'