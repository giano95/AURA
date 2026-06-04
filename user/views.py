from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Coach, Client, User

from .forms import SignupUserForm, SignupCoachInfoForm, SignupClientInfoForm, UserLoginForm


def signup_role(request):
    role = request.POST.get("role")
    request.session["signup_role"] = role
    return redirect("user_signup", 2)


def signup_info(request):
    role = request.session.get('signup_role')

    if role == 'coach':
        form = SignupCoachInfoForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data.get('first_name')
            request.session['last_name'] = form.cleaned_data.get('last_name')
            request.session['phone_number'] = form.cleaned_data.get('phone_number')
            request.session['bio'] = form.cleaned_data.get('bio')
            return redirect("user_signup", 3)
        else:
            messages.error(request, 'Form is not valid')
            return redirect("user_signup", 2)
    elif role == "client":
        form = SignupClientInfoForm(request.POST)
        if form.is_valid():
            request.session['first_name'] = form.cleaned_data.get('first_name')
            request.session['last_name'] = form.cleaned_data.get('last_name')
            request.session['phone_number'] = form.cleaned_data.get('phone_number')
            request.session['goals'] = form.cleaned_data.get('goals')
            return redirect("user_signup", 3)
        else:
            messages.error(request, 'Form is not valid')
            return redirect("user_signup", 2)
    else:
        return redirect("user_signup", 1)


def signup_user(request):
    user = None
    form = SignupUserForm(request.POST)
    role = request.session.get("signup_role")

    if not form.is_valid():
        print("Form is not valid:", form.errors)
        messages.error(request, 'Form is not valid')
        # request.session.flush()
        return redirect('user_signup', 3)

    email = form.cleaned_data.get('email')
    password = form.cleaned_data.get('password1')

    if role == 'coach':
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
        phone_number = request.session.get('phone_number')
        bio = request.session.get('bio')
        user = User.objects.create_user(email=email, password=password, is_user_a_coach=True, first_name=first_name,
                                        last_name=last_name)
        Coach.objects.create(user=user, phone_number=phone_number, bio=bio)
    elif role == "client":
        first_name = request.session.get('first_name')
        last_name = request.session.get('last_name')
        phone_number = request.session.get('phone_number')
        goals = request.session.get('goals')
        user = User.objects.create_user(email=email, password=password, is_user_a_coach=False, first_name=first_name,
                                        last_name=last_name)
        Client.objects.create(user=user, phone_number=phone_number, goals=goals)
    else:
        return redirect('user_signup', 1)

    if user is None:
        messages.error(request, 'Something went wrong during user creation')
        request.session.flush()
        return redirect('user_signup', 1)

    user = authenticate(request, username=email, password=password)

    if user is None:
        messages.error(request, 'Something went wrong during user authentication')
        User.objects.get(email=email).delete()
        return redirect('user_signup', 3)

    login(request, user)
    request.session.flush()
    return redirect('home')


def signup(request, step):
    if request.method == "POST":
        if step == 1:
            return signup_role(request)
        elif step == 2:
            return signup_info(request)
        elif step == 3:
            return signup_user(request)
        else:
            messages.error(request, 'Wrong signup_step')
            request.session.flush()
            return redirect('signup', 1)
    else:  # GET
        form = None
        if step == 1:
            pass
        elif step == 2:
            if request.session["signup_role"] == "coach":
                form = SignupCoachInfoForm()
            elif request.session["signup_role"] == "client":
                form = SignupClientInfoForm()
            else:
                return redirect('user_signup', 1)
        elif step == 3:
            form = SignupUserForm()

        return render(
            request,
            'user/signup.html',
            {
                'form': form,
                'role': request.session.get('signup_role'),
                'step_names': ['Choose role', 'Your information', 'Account'],
            }
        )


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if not form.is_valid():
            print(form.errors)
            messages.error(request, 'Form is not valid')
            return render(request, 'user/login.html', {'form': form})

        form.clean()
        login(request, form.get_user())
        return redirect('home')

    else:
        form = UserLoginForm()
        return render(request, 'user/login.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        pass
    else:
        pass
    return redirect('home')
