from django.db import models
from account.choices import UserTypeChoices
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager


class UserAccountManager(BaseUserManager):
    
    def create_user(self, email, password):
        if not email or len(email) <= 0 : 
            raise  ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        
        user = self.model(
            email=email.lower()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self , email , password):
        user = self.create_user(
            email=email.lower(),
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
    

class UserAccount(AbstractBaseUser):
    user_type = models.CharField(max_length=10, choices=UserTypeChoices, default=UserTypeChoices.student)
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    is_active = models.BooleanField(default = True)
    is_admin = models.BooleanField(default = False)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    
    USERNAME_FIELD = "email"

    objects = UserAccountManager()
 
    def __str__(self):
        return str(self.email)
    
    def has_perm(self , perm, obj = None):
        return self.is_admin
    
    def has_module_perms(self , app_label):
        return True
    
    def save(self , *args , **kwargs):
        if not self.user_type:
            self.user_type = UserTypeChoices.student
        return super().save(*args , **kwargs)


class ExpertManager(models.Manager):
    def create_user(self, email, password):
        if not email: 
            raise ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        user = self.model(
            email=email.lower()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(user_type=UserTypeChoices.expert)
        return queryset
    

class Expert(UserAccount):
    class Meta:
        proxy = True    
    objects = ExpertManager()

    def save(self, *args, **kwargs):
        self.user_type = UserTypeChoices.expert
        return super().save(*args, **kwargs)


class StudentManager(models.Manager):
    def create_user(self, email, password):
        if not email:
            raise ValueError("Email field is required !")
        if not password :
            raise ValueError("Password is must !")
        user = self.model(
            email=email.lower()
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs).filter(user_type=UserTypeChoices.student)
        return queryset
    

class Student(UserAccount):
    class Meta:
        proxy = True
    objects = StudentManager()

    def save(self, *args, **kwargs):
        self.user_type = UserTypeChoices.student
        return super().save(*args, **kwargs)
