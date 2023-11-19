from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.views import View
from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.contrib.messages import success, warning, info, error, debug
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import AppTokenGenerator
from json import loads
from validate_email import validate_email

token_generator = AppTokenGenerator()

# Create your views here.
class UsernameValidationView(View):
    def post(self, request):
        data = loads(request.body)
        username = data['username']
        
        if not str(username).isalnum():
            return JsonResponse({ 'username_error': 'Username should only contain alphanumeric characters'}, status = 400)
               
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'sorry username in use, choose another one' }, status = 409)
       
        return JsonResponse({'username_valid': True})

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        try:
            # get user data -> validate -> create a user account
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            context = {'fieldValues': request.POST}
            
            if not User.objects.filter(username = username).exists():
                #if not User.objects.filter(email = email).exists():          
                    if 0 < len(password) < 8:
                        error(request, "Password too Short")
                        return render(request, 'authentication/register.html', context = context)

                    elif len(password) == 0:
                        error(request, "Please type a password")
                        return render(request, 'authentication/register.html', context = context)

                    elif not str(password[0]).isupper():
                        error(request, 'The first letter should be Capital')
                        return render(request, 'authentication/register.html', context = context)

                    user = User.objects.create_user(username = username, email = email)
                    user.set_password(password)
                    user.is_active = False
                    user.save()
                    
                    # path to view -> getting domain we are on -> relative url to verification -> encode uid -> token
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain # 127.0.0.1:8000
                    link = reverse('activate', kwargs = {'uidb64': uidb64, 'token': token_generator.make_token(user)})
                    activate_url = "http://" + domain + link
                    
                    email_subject = "Your Account Activation"
                    email_body = 'Hi' + user.username + ", Please use this link to verify your account.\n" + activate_url
                    email_from = "noreply@gmail.com"  # Replace with your email address
                    email_to = [email]
                    email = EmailMessage(email_subject, email_body, email_from, email_to)
                    email.send(fail_silently = False)
                    
                    success(request, "Account successfully created!")
                         
                #else: error(request, "User with this Email already exists.")

            else: error(request, "User with this username already exists.")

            return render(request, 'authentication/login.html')

        except Exception as e:
            error(request, f"An error occurred: {str(e)}")
            return render(request, 'authentication/register.html')
    
class EmailValidationView(View):
    def post(self, request):
        data = loads(request.body)
        email = data['email']
        
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid' }, status = 400)
               
        # if User.objects.filter(email = email).exists():
        #     return JsonResponse({'email_error': 'Sorry emial in use, choose another one' }, status = 409)
       
        return JsonResponse({'email_valid': True})
    
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = int(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk = id)
            
            if not token_generator.check_token(user, token):
                return redirect('login?message=User already activated')
            
            if user.is_active:
                return redirect('login')
            
            user.is_active = True
            user.save()
            
            success(request, "Account activated successfully")
            return redirect("login")
            
        except Exception as ex:
            pass
        
class LogInView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        
        if username and password:
            user = authenticate(username = username, password = password)
            
            if user:
                if user.is_active:
                    login(request, user)
                    success(request, f"Welcome, {user.username} you are now logged in")
                    return redirect("expenses")
   
                error(request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            
            error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')
        
        error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')
    
class LogOutView(View):
    def post(self, request):
        logout(request)
        success(request, "you have been logged out")
        return redirect('login')