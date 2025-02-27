from django.contrib import admin
from . import models
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives



class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'job_seeker', 'status', 'applied_on')

    def save_model(self, request, obj, form, change):
        obj.save()
        if obj.status == "Accepted":
            email_subject = "Your Job Application Is Accepted Congratulations"
            email_body = render_to_string('admin_email.html', {'user' : obj.job_seeker.user})
            email = EmailMultiAlternatives(email_subject, '', to=[obj.job_seeker.user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()

    

admin.site.register(models.Application, ApplicationAdmin)