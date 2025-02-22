from django.db import models
from rest_framework.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser


class UserProfile(models.Model):
    bio = models.CharField (null=True, blank=True, max_length=128)
    image = models.ImageField(upload_to='user.image/')
    website = models.URLField(null=True, blank=True)
    age = models.PositiveSmallIntegerField(validators=[MinValueValidator(15),
                                                       MaxValueValidator(70)], null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)


    def __str__(self):
        return f'{self.first_name}, {self.last_name}'
    

class Follow(models.Model):
    follower = models.ManyToManyField(UserProfile,  on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.follower}, {self.following}'

class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user.post/')
    video = models.FileField(upload_to='user_video/')
    description = models.CharField(max_length=256, null=True, blank=True)
    hashtag = models.CharField(max_length=64, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}. {self.hashtag}'
    
    def clean(self):
        super().clean()
        if not self.image and not self.video:
            raise ValidationError('Choose correct number of image/video!')

    def get_count_like(self):
        return self.post_like.count()

class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ManyToManyField(Post,  on_delete=models.CASCADE)
    like = models.BooleanField()
    created_at =  models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user}, {self.post}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.CharField(max_length=256, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}, {self.post}'

class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,  on_delete=models.CASCADE)
    like = models.BooleanField()
    created_at =  models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment')

    def __str__(self):
        return f'{self.user} liked {self.comment}'

class Story(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story_image/')
    video = models.FileField(upload_to='story_video/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user}'


class Saved(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class SavedItem(models.Model):
    post = models.ManyToManyField(Post, on_delete=models.CASCADE)
    save = models.ManyToManyField(Saved, on_delete=models.CASCADE )
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'saved')

    def __str__(self):
        return f'{self.post} liked {self.saved}'
    
class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_at = models.DateField(auto_now_add=True)


class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.FileField(upload_to='videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
