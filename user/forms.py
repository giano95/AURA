from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from user.models import User, Coach, Client, Profile
from django.core.validators import RegexValidator

tailwind_input_class = 'block w-full rounded-md dark:bg-white/5 bg-black/5 px-3 py-1.5 text-base dark:text-white text-black ' \
                       'outline-1 -outline-offset-1 dark:outline-white/10 outline-black/15 placeholder:text-gray-500 ' \
                       'focus:outline-2 focus:-outline-offset-2 focus:outline-indigo-500 sm:text-sm/6 '


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=20,
        label='First Name:',
        widget=forms.TextInput(attrs={'class': tailwind_input_class, 'placeholder': 'John'})
    )
    last_name = forms.CharField(
        max_length=20,
        label='Last Name:',
        widget=forms.TextInput(attrs={'class': tailwind_input_class, 'placeholder': 'Smith'})
    )
    phone_number = forms.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Regex for international phone numbers
                message="Phone number must be entered in the format: '+223334445555'. Up to 15 digits allowed."
            )
        ],
        label='Phone number:',
        widget=forms.TextInput(attrs={'class': tailwind_input_class, 'placeholder': '+223334445555'})
    )

    class Meta:
        model = Profile
        fields = (
            'first_name',
            'last_name',
            'phone_number',
        )


class SignupCoachInfoForm(ProfileForm):
    bio = forms.CharField(
        label='Bio:',
        widget=forms.TextInput(attrs={'class': tailwind_input_class, 'placeholder': 'Tell something about yourself...'})
    )

    class Meta:
        model = Coach
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'bio',
        )


class SignupClientInfoForm(ProfileForm):
    goals = forms.CharField(
        label='Goals:',
        widget=forms.TextInput(
            attrs={'class': tailwind_input_class, 'placeholder': "Tell us how you're gonna aura farm..."})
    )

    class Meta:
        model = Client
        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'goals',
        )


class SignupUserForm(UserCreationForm):
    email = forms.EmailField(
        label='Email address:',
        widget=forms.TextInput(attrs={'class': tailwind_input_class, 'placeholder': 'name@example.com'})
    )
    password1 = forms.CharField(
        max_length=20,
        label='Password:',
        widget=forms.PasswordInput(attrs={'class': tailwind_input_class, 'placeholder': ''})
    )
    password2 = forms.CharField(
        max_length=20,
        label='Password Confirmation:',
        widget=forms.PasswordInput(attrs={'class': tailwind_input_class, 'placeholder': ''})
    )

    class Meta:
        model = User
        fields = (
            'email',
            'password1',
            'password2'
        )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email address:',
        widget=forms.TextInput(attrs={'class': tailwind_input_class, 'placeholder': 'name@example.com'})
    )
    password = forms.CharField(
        max_length=20,
        label='Password:',
        widget=forms.PasswordInput(attrs={'class': tailwind_input_class, 'placeholder': ''})
    )

    class Meta:
        model = User
        fields = (
            'username',
            'password',
            'error_messages',
        )
