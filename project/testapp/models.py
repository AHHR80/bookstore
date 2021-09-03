from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

from datetime import datetime



class MyUserManager(BaseUserManager):
    def create_user(self, email, name, lastname, phone, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have an email address')

        if not lastname:
            raise ValueError('Users must have an email address')

        if not phone:
            raise ValueError('Users must have an email address')

        if not password:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            lastname=lastname,
            phone=phone,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, lastname, phone, password=None):
        user = self.create_user(email, name, lastname,phone, password)

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

def image_path(self, filename):
    return "userprofile/{}/image.amir.png".format(self.pk)

class MyUser(AbstractBaseUser):


    email = models.EmailField(default='amir', unique=True)
    name = models.CharField(max_length=150, default='amir')
    lastname = models.CharField(max_length=150, default='amir')
    phone = models.IntegerField(unique=True)
    data_join= models.DateTimeField(verbose_name='data join' ,auto_now_add=datetime.now())
    last_login= models.DateTimeField(verbose_name='last login' ,auto_now=True)
    profile_image = models.ImageField(null=True, blank=True, upload_to= image_path)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone', 'name', 'lastname']

    objects = MyUserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
