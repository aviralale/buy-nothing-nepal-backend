from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            username,
            first_name,
            last_name,
            phone_number,
            password=None,
            **extra_fields,
    ):
        if not email:
            raise ValueError('Users must have an email address')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')
        if not phone_number:
            raise ValueError('Users must have a phone number')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(
            self,
            email,
            username,
            first_name,
            last_name,
            phone_number,
            password=None,
            **extra_fields,
            ):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_superuser") is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        if extra_fields.get("is_staff") is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get("is_admin") is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self.create_user(
            email,
            username,
            first_name,
            last_name,
            phone_number,
            password,
            **extra_fields,
            )
    

class User(AbstractBaseUser):
    GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]


    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        )
    username = models.CharField(
        max_length=255,
        unique=True,
        )
    first_name = models.CharField(
        max_length=255,
        )
    last_name = models.CharField(
        max_length=255,
        )
    phone_number = models.CharField(
        max_length=255,
        )
    
    profile_picture = models.ImageField(
        upload_to='profile_pictures',
        blank=True,
        null=True,
        )

    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)

    is_active = models.BooleanField(
        default=False,
        )
    is_staff = models.BooleanField(
        default=False,
    )
    is_admin = models.BooleanField(
        default=False,
        )
    is_superuser = models.BooleanField(
        default=False,
    )
    date_joined = models.DateTimeField(
        default=timezone.now,
        )
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']
    def __str__(self):
        return self.username
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, app_label):
        return self.is_superuser
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    

