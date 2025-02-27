from rest_framework import serializers
from django.contrib.auth.models import User
from employee.models import Employee
from job_seeker.models import JobSeeker


USER_TYPES = [
    ('Job_seeker', 'Job_seeker'),
    ('Employee', 'Employee')
]


class RagistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=USER_TYPES)
    profile_image = serializers.ImageField(required=False, allow_null=True)

    company_name = serializers.CharField(required=False, allow_blank=True)
    company_description = serializers.CharField(required=False, allow_blank=True)
    logo = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'password', 'confirm_password', 'profile_image', 'company_name', 'company_description', 'logo']
    
    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        role = self.validated_data['role']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        profile_image = self.validated_data.get('profile_image', None)

        company_name = self.validated_data.get('company_name', None)
        company_description = self.validated_data.get('company_description', None)
        logo = self.validated_data.get('logo', None)

        # print("Serializer Role: ", role) 

        # if password != password2:
        #     raise serializers.ValidationError({'error': "Password did not match"})
        
        # if User.objects.filter(email=email).exists():
        #     raise serializers.ValidationError({'error': "This email already exists"})
        # updatecode
        errors = {}

        if password != password2:
            errors['confirm_password'] = "Passwords do not match"

        if User.objects.filter(email=email).exists():
            errors['email'] = "This email already exists"

        if User.objects.filter(username=username).exists():
            errors['username'] = "This username is already taken"

        if errors:
            raise serializers.ValidationError(errors)
        
        account = User(email=email, username=username, first_name=first_name, last_name=last_name)
        account.set_password(password)
        # account.is_active = False
        account.is_active = True
        account.save()

        # Handle user role and profile creation
        if role == 'Job_seeker':
            job_seeker = JobSeeker.objects.create(user=account)
            if profile_image:
                job_seeker.profile_image = profile_image
                job_seeker.save()

        elif role == 'Employee':
            employee = Employee.objects.create(user=account)
            if profile_image:
                employee.profile_image = profile_image

                employee.company_name=company_name
                employee.company_description=company_description
                employee.logo=logo
                employee.save()

        return account


class UserloginSerializer(serializers.Serializer):
    username = serializers.CharField(required = True)
    password = serializers.CharField(required = True)



class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Incorrect old password!!")
        return value
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password character maxium more then 8 character")
        return value
    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()