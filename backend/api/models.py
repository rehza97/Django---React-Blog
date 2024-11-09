from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.text import slugify
from shortuuid.django_fields import ShortUUIDField
import shortuuid
from users.models import *
# Create your models h
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    image = models.FileField(
        upload_to='image/categories', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

        class Meta:
            ordering = ['-date']
            varbose_name_plural = "Categories"

    def post_count(self):
        return Post.objects.filter(category=self).count()


class Post(models.Model):
    STATUS = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Disabled', 'Disabled'),

    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Draft")
    view = models.IntegerField(default=0)
    likes = models.ManyToManyField(User, blank=True, related_name='likes_user')
    image = models.FileField(upload_to='image/post', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = f"{slugify(self.title)}-{shortuuid.uuid()[:2]}"
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-date']



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    comment = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.post.title

    class Meta:
        ordering = ['-date']


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.post.title

    class Meta:
        ordering = ['-date']


class Notification(models.Model):
    NOTI_TYPE = (
        ('like', 'like'),
        ('Comment', 'Comment'),
        ('Bookmark', 'Bookmark'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=NOTI_TYPE)
    seen = models.BooleanField(default=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.post:
            return f"{self.type} -> {self.post.title}"
        else:
            return "Notification"

    class Meta:
        ordering = ['-date']


