from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializer

class ContactMessageViewset(viewsets.ModelViewSet):
    queryset = models.ContactMessage.objects.all()
    serializer_class = serializer.ContactMessageSerializer