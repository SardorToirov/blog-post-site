from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from ckeditor.fields import RichTextField

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')

STATUS_Q = (
    ('draft', 'Draft'),
    ('published', 'Published')
)

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    likes = models.SmallIntegerField(default=0)
    body = RichTextField()
    create = models.DateTimeField(auto_now_add=True)
    publish = models.DateTimeField(auto_now=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, choices=STATUS_Q, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home:post_detail', args=[
            self.publish.year, self.publish.month, self.publish.day, self.slug
        ])

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body[:20]}... by {self.name}'

    def get_absolute_url(self):
        return reverse('home:post_detail', kwargs={
            'year': self.post.publish.year,
            'month': self.post.publish.month,
            'day': self.post.publish.day,
            'slug': self.post.slug
        })
