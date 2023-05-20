from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from phonenumber_field.phonenumber import PhoneNumber



class AchareUserManager(BaseUserManager):
    def create_user(self, phone_number, email, first_name=None, last_name=None, password=None):
        if phone_number is None:
            raise ValueError("Phone number is None")
        reversed_phonenumber = PhoneNumber.from_string(phone_number, region="IR")
        if not reversed_phonenumber.is_valid():
            raise ValueError("Phone number is Invalid")
        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, phone_number, email, first_name=None, last_name=None,password=None):
        user = self.create_user(phone_number, email, first_name, last_name, password)
        user.is_admin = True
        user.save(using=self._db)
        return user




class AchareUser(AbstractBaseUser):
    phone_number = PhoneNumberField(unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ['email']

    objects = AchareUserManager()

    @property
    def is_superuser(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_superuser(self):
        return self.is_admin
    
    @property
    def is_staff(self):
        return self.is_active
    
    def __str__(self) -> str:
        return f"{self.phone_number}"
