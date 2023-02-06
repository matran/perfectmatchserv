import uuid
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from datetime import datetime
from django.dispatch import receiver
from django.urls import reverse
from django.core.mail import send_mail  
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from cloudinary.models import CloudinaryField
def upload_to(instance, filename):
    return 'profilepics/{filename}'.format(filename=filename)
class UserManager(BaseUserManager):
    def create_user(self,email, password=None):
        if not email:
            raise ValueError('Users Must Have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email, password):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active=True
        user.save()
        return user
class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(verbose_name='email address',max_length=255,unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()
    def __str__(self):
        return self.email
    class Meta:
        db_table = "login"
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, primary_key = True)
    isactive=models.BooleanField(default=False)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    age=models.IntegerField()
    religion=models.CharField(max_length=30)
    bio=models.TextField(null=True)
    relationtype=models.CharField(max_length=50)
    paymentid=models.TextField(null=True)
    subscriptiontype=models.CharField(max_length=50,null=True)
    subscription=models.CharField(max_length=50,null=True)
    email = models.EmailField(verbose_name='email',max_length=255,unique=True)
    photo1= CloudinaryField('photo1',null=True) 
    photo2=CloudinaryField('photo2',null=True) 
    photo3=CloudinaryField('photo3',null=True) 
    photo4= CloudinaryField('photo4',null=True) 
    photo5=CloudinaryField('photo5',null=True) 
    reportlist=models.TextField(null=True,default="[]")
    blocklist=models.TextField(null=True,default="[]")
    timestamp=models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = "userprofile"

class FriendRequests(models.Model):
    fromuserid=models.IntegerField()
    touserid=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = "friendrequests"

class Matches(models.Model):
    userid=models.IntegerField()
    otheruserid=models.IntegerField()
    chatid=models.TextField()
    class Meta:
        db_table = "matches"


class ReportedUsers(models.Model):
    userid= models.IntegerField()
    name=models.CharField(max_length=50)
    reportedby=models.CharField(max_length=50)
    reportedbyid=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = "reportedusers"

class Subscriptions(models.Model):
    userid = models.IntegerField()
    subscription = models.CharField(max_length=50)
    subscriptiontype=models.CharField(max_length=50)
    expirydate=models.DateTimeField(blank=True)
    amount=models.DecimalField(default=0.00,max_digits=20,decimal_places=2,validators=[MinValueValidator(0)])
    ispaid=models.BooleanField(default=False)
    timestamp=models.DateTimeField(auto_now_add=True, blank=True)
    class Meta:
        db_table = "subscriptions"