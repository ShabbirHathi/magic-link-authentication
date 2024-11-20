from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import logout
from django.contrib import messages

from django.conf import settings
from app1.models import UserData
from app1.email import send_mail
from urllib.parse import urljoin
from datetime import timedelta
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

# Create your views here.

# Set the encryption key. --- Replace the 'very-secret-token-key'
s = URLSafeTimedSerializer('very-secret-token-key')

# Encrypt and decrypt with timed encryption for itsdangerous
def encryptKey(email):
    return s.dumps(email)

def decryptKey(key, max_age=3600):
    try:
        return s.loads(key, max_age=max_age)
    except SignatureExpired:
        print("Sig out of date")
        return False
    except BadSignature:
        print("bad signature")
        return False

def loginview(request: HttpRequest):
    if request.method == 'POST':
        try:
            email = request.POST.get("your_email")
            user = UserData.objects.filter(email=email)

            verification_token = encryptKey(email)

            if user:
                user[0].email_verification_token = verification_token
                user[0].save()
            else:
                UserData.objects.create(email=email, email_verification_token=verification_token)

            # Get the current site's domain
            current_site = get_current_site(request)
            server_url = f"http://{current_site.domain}"
            
            # Create the magic URL
            magic_url = urljoin(server_url, f'validate?t={verification_token}')
            print("Magic link")
            print(magic_url)
            print()
            print()
            send_mail(email, magic_url)
            
            messages.success(request, "Login link has been sent to your provided email account. Please check! It will be active for 1 hour.")

        except Exception as e:
            messages.success(request, str(e))

    return render(request, 'login.html')

def logoutview(request):
    if 'user_email' in request.session:
        del request.session['user_email']
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('login')

def validateview(request: HttpRequest):
    token = request.GET.get('t')
    if token:
        # Assuming decryptKey is a function you've defined to decrypt the token
        email = decryptKey(token, max_age=600)  # max_age=600 means token is valid for 10 minutes
        if email:
            query = UserData.objects.filter(email_verification_token=token).first()
            if query.email == email:
                generated_date = query.created_at
                current_datetime = now()
                # Check if the token is older than 1 hour
                if current_datetime - generated_date > timedelta(hours=1):
                    return HttpResponse("Signature expired")
                else:
                    # Store email in session to indicate the user is logged in
                    request.session['user_email'] = email
                    return redirect('dashboard')
        else:
            return HttpResponse("Invalid token or email")
    else:
        return HttpResponse("No token provided.")
 
 

from django.http import HttpResponseRedirect
from django.urls import reverse

def custom_login_required(function):
    def wrapper(request, *args, **kwargs):
        # Check if user email is in session (indicating they are logged in)
        if 'user_email' not in request.session:
            return HttpResponseRedirect(reverse('login'))  # Redirect to login if not logged in
        return function(request, *args, **kwargs)
    return wrapper
  
@custom_login_required
def dashboardview(request):

    return render(request,"dashboard.html")


