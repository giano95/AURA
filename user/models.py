from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Superuser must have an email address")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_superuser = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractUser):
    username = models.CharField(blank=True, null=True, max_length=50)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    is_user_a_coach = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    phone_number = models.CharField(
        max_length=15,
        blank=True, null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',  # Regex for international phone numbers
                message="Phone number must be entered in the format: '+223334445555'. Up to 15 digits allowed."
            )
        ]
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Coach(Profile):
    bio = models.TextField()

    class Meta:
        verbose_name_plural = "Coaches"


class Client(Profile):
    goals = models.TextField(blank=True)
    weight = models.DecimalField(decimal_places=1, max_digits=4, blank=True, null=True)
    height = models.DecimalField(decimal_places=2, max_digits=3, blank=True, null=True)
