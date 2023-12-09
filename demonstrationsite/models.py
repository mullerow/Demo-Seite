from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.core.validators import MinLengthValidator

class UserImageModel(models.Model):
    image = models.ImageField(upload_to='user_image/', blank=False)

    class Meta:
        verbose_name = 'Image'
        verbose_name_plural = 'Images'
    def __str__(self):
        return str(self.image)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100,unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    salutation = models.CharField(max_length=13, default='keine Angabe')
    it_reference = models.CharField(max_length=100)
    about_me = models.TextField(max_length=300, blank=True)
    profile_image = models.ForeignKey(UserImageModel, on_delete=models.CASCADE, null=True, blank=True, default='14')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username

class PostModel(models.Model):
    category = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    experience = models.IntegerField(default=0)
    short_description = models.CharField(max_length=200, null=True)
    post_text = models.TextField(max_length=5000, null=True)
    post_date = models.DateField(auto_now=True)
    post_image = models.ImageField(upload_to='post_image/', default='default_image.png')
    slug = models.SlugField(unique=True, default='', null=False, editable=False)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class IndexCommentModel(models.Model):
    comment_username = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    comment_text = models.TextField(max_length=1000, validators=[MinLengthValidator(5)])
    comment_date = models.DateField(auto_now=True)
    comment_it_reference = models.CharField(max_length=100, null=True)
    comment_image = models.ImageField(upload_to='comment_image', null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f"{self.comment_username}  {self.comment_date}"

class VisitorCountModel(models.Model):
    count = models.IntegerField(default=0)

