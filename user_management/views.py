from . import serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


class UserRagistrationApiView(APIView):
    serializer_class = serializer.RagistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        print("line 23",serializer)
        if serializer.is_valid():
            role = serializer.validated_data.get('role')  # Get role
            print("Role:", role)  # Print role for debugging
            # print(serializer.profile_image)
            profile_image = serializer.validated_data.get('profile_image', None)
            company_name = serializer.validated_data.get('company_name', None)
            print("line 27",company_name)
            user = serializer.save()
            token = default_token_generator.make_token(user)
            print("token : ", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("Uid : ", uid)
            # confirm_link = f"http://127.0.0.1:8000/user/active/{uid}/{token}/"
            # email_subject = "Confirm Your mail"
            # email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            # email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            # email.attach_alternative(email_body, 'text/html')
            # email.send()
            return Response({"success": "Registration Successfully!! Please Login!!"}, status=status.HTTP_201_CREATED)
            # return Response("Check you mail for confirmation")
        return Response(serializer.errors)


def activate(request, uid64, token):
    next_url = request.GET.get("next", "http://127.0.0.1:5500/login.html")
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except (User.DoesNotExist, ValueError):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect(next_url)
    else:
        return HttpResponseRedirect("http://127.0.0.1:5500/sign_up.html")


class UserloginApiview(APIView):
    def post(self, request):
        serializers = serializer.UserloginSerializer(data=self.request.data)
        if serializers.is_valid():
            username = serializers.validated_data['username']
            password = serializers.validated_data['password']

            user = authenticate(username=username, password=password)
            print("user", user)

            if user:
                token, _ = Token.objects.get_or_create(user=user)
                
                # Get profile image based on role
                profile_image = None
                role = None
                jobseekerid = None
                if hasattr(user, 'job_seeker'):
                    profile_image = user.job_seeker.profile_image.url if user.job_seeker.profile_image else None
                    jobseekerid = user.job_seeker.id
                    role = 'Job_seeker'
                elif hasattr(user, 'employee'):
                    profile_image = user.employee.profile_image.url if user.employee.profile_image else None
                    role = 'Employee'
                # print("login view")
                # print("views ", role)
                # print("token ", token)
                # print("userid ", user.id)
                print("jobseekrid : ",jobseekerid)
                response_data = {
                    'token': token.key,
                    'user_id': user.id,
                    'profile_image': profile_image,
                    'role': role,
                    'username' : username,
                    'job_seeker_id':jobseekerid,
                }
                login(request, user)
                return Response(response_data)
            
            # Invalid credentials response
            return Response(
                {'error': "Invalid username or password!"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Userlogoutview(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return redirect('login')
    



class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializers = serializer.PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializers.is_valid():
            serializers.save()
            return Response({"message": "Password update successfully!!"}, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)