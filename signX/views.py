from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Patient, Doctor, Address


def home(request):
    """Home page view"""
    return render(request, 'home.html')


@require_http_methods(["GET", "POST"])
def signup(request):
    """Handle user signup for both Patient and Doctor"""
    # Get user_type from query parameter if available
    user_type_param = request.GET.get('user_type', '')

    if request.method == 'POST':
        # Get form data
        user_type = request.POST.get('user_type')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        profile_picture = request.FILES.get('profile_picture')
        address_line1 = request.POST.get('address_line1')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')

        # Validation
        errors = []

        # Check if user type is selected
        if not user_type or user_type not in ['patient', 'doctor']:
            errors.append('Please select a valid user type.')

        # Check if passwords match
        if password != confirm_password:
            errors.append('Passwords do not match.')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists.')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append('Email already exists.')

        # If there are errors, show them
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'signup.html')

        try:
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Create address
            address = Address.objects.create(
                line1=address_line1,
                city=city,
                state=state,
                pincode=pincode
            )

            # Create patient or doctor profile
            if user_type == 'patient':
                Patient.objects.create(
                    user=user,
                    profile_picture=profile_picture,
                    address=address
                )
            else:  # doctor
                Doctor.objects.create(
                    user=user,
                    profile_picture=profile_picture,
                    address=address
                )

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('login')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'signup.html', {'user_type': user_type_param})

    return render(request, 'signup.html', {'user_type': user_type_param})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Handle user login"""
    # Get user_type from query parameter if available
    user_type_param = request.GET.get('user_type', '')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to get user by email first
        try:
            if '@' in username:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
        except User.DoesNotExist:
            pass

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Determine user type
            if hasattr(user, 'patient_profile'):
                user_type = 'patient'
            elif hasattr(user, 'doctor_profile'):
                user_type = 'doctor'
            else:
                messages.error(request, 'Invalid account type.')
                return render(request, 'login.html', {'error': 'Invalid account type.'})

            # Login user
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')

            # Redirect to appropriate dashboard
            if user_type == 'patient':
                return redirect('patient_dashboard')
            else:
                return redirect('doctor_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html', {'error': 'Invalid username or password.', 'user_type': user_type_param})

    return render(request, 'login.html', {'user_type': user_type_param})


@login_required(login_url='login')
def patient_dashboard(request):
    """Patient dashboard view"""
    try:
        patient = request.user.patient_profile
    except Patient.DoesNotExist:
        messages.error(request, 'You are not registered as a Patient.')
        return redirect('login')

    context = {
        'patient': patient,
    }
    return render(request, 'patient_dashboard.html', context)


@login_required(login_url='login')
def doctor_dashboard(request):
    """Doctor dashboard view"""
    try:
        doctor = request.user.doctor_profile
    except Doctor.DoesNotExist:
        messages.error(request, 'You are not registered as a Doctor.')
        return redirect('login')

    context = {
        'doctor': doctor,
    }
    return render(request, 'doctor_dashboard.html', context)


@login_required(login_url='login')
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')
