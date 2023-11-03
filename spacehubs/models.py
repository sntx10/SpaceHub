from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from feedback.models import Like, Favorite, Comment
from account.models import Category
from pytils.translit import slugify

# Create your models here.

User = get_user_model()


class Tag(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class News(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="news")
    favorites = GenericRelation(Favorite)
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)
    views_count = models.PositiveIntegerField(default=0)
    date_posted = models.DateField(auto_now=True)
    expanded_date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blogs")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="blogs")
    views_count = models.PositiveIntegerField(default=0)
    favorites = GenericRelation(Favorite)
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)
    date_posted = models.DateField(auto_now=True)
    expanded_date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.TextField()
    views_count = models.PositiveIntegerField(default=0)
    favorites = GenericRelation(Favorite)
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)
    date_posted = models.DateField(auto_now=True)
    expanded_date_posted = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PodCast(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    views_count = models.PositiveIntegerField(default=0)
    favorites = GenericRelation(Favorite)
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    audio_file = models.FileField(upload_to="podcasts/")
    date_posted = models.DateField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    expanded_date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    code = models.FileField(upload_to="codes/")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    views_count = models.PositiveIntegerField(default=0)
    favorites = GenericRelation(Favorite)
    likes = GenericRelation(Like)
    comments = GenericRelation(Comment)
    date_posted = models.DateField(auto_now=True)
    expanded_date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} viewed the project "{self.project}" at {self.viewed_at}'


class BlogView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} viewed the blog "{self.blog}" at {self.viewed_at}'


class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} viewed the post "{self.post}" at {self.viewed_at}'


class PodCastView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    podcast = models.ForeignKey(PodCast, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} listened to the podcast "{self.podcast}" at {self.viewed_at}'


class NewsView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} read the news "{self.news}" at {self.viewed_at}'



