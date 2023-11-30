from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout

from app.forms import CustomUserCreationForm, UserLoginForm
from app.models import Customuser

# Create your views here.

def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password2'])
            user.generate_token()
            user.email_verification()
            user.save()
            messages.success(
                request, 'User registered successfully. Please check your email for verification.')
            return redirect('register')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})



def verify_account(request):
    token = request.GET.get('token')

    if token:
        user = get_object_or_404(Customuser, verification_token=token)

        if not user.is_active:
            user.is_active = True
            user.save()
            messages.success(
                request, 'Account verified successfully. You can now log in.')

            # Delete the verification token from the user instance
            user.verification_token = None
            user.save()
        else:
            messages.info(request, 'Account already verified. You can log in.')
    else:
        messages.error(request, 'Invalid verification token.')

    return redirect('login')




def custom_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            remember_me = form.cleaned_data.get('remember_me')
            if not remember_me:
                # Session expires when the browser is closed
                request.session.set_expiry(0)

            user = form.get_user()
            login(request, user)
            # Change 'home' to the desired redirect after login
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'login.html', {'form': form})



def custom_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request,"home.html")