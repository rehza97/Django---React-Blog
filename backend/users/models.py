from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
import shortuuid
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=200 , unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200 , blank=True , null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def save(self ,*args, **kwargs):
        email_username , email_domain = self.email.split('@') 
        if self.full_name == '' or self.full_name == None:
            self.full_name = email_username    
        if self.username == '' or self.username == None :
            self.username = email_username
        if self.username is not None:
            self.username = f"{self.username} {shortuuid.uuid()[:2]}"
        super(User , self).save(*args, **kwargs)
        
    def __str__(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.FileField(upload_to='image/profile' , default='default/user.jpg' , null=True , blank=True)
    full_name = models.CharField(max_length=200 , blank=True , null=True)
    bio = models.CharField(max_length=200 , blank=True , null=True)
    about = models.CharField(max_length=200 , blank=True , null=True)
    auther = models.BooleanField(default=False)
    contry = models.CharField(max_length=200 , blank=True , null=True)
    facebook = models.CharField(max_length=200 , blank=True , null=True)
    X = models.CharField(max_length=200 , blank=True , null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    def save(self ,*args, **kwargs):
        if self.user.full_name == '' or self.user.full_name == None:
            self.full_name = self.user.full_name    
        
        super(Profile , self).save(*args, **kwargs)
        
    def __str__(self):
        return self.user.username
    

def create_user_profile(sender , instance , created , **kwargs):
    if created:
        Profile.objects.create(user=instance)
def save_user_profile(sender , instance ,**kwargs):
    instance.profile.save()
post_save.connect(create_user_profile , sender=User)
post_save.connect(save_user_profile , sender=User)

