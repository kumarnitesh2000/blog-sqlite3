from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')
class Post(models.Model):
    CHOICE = (
        ('draft','Draft'),('published','Published'),
    )
    title=models.CharField(max_length=250)
    publish=models.DateTimeField(default=timezone.now)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    slug=models.SlugField(max_length=250,unique_for_date='publish')
    status=models.CharField(max_length=20,
                            choices=CHOICE,default='draft')
    author=models.ForeignKey(User,on_delete=models.CASCADE,
                             related_name='blog')
    body=models.TextField()
    #the default manager (objects)
    objects=models.Manager()
    #our custom manager (published->this name we decided)
    published=PublishedManager()
    #now here is the example for the use in place of default manager
    #Post.published.filter(title__startswith='who')
    tags = TaggableManager()
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                     args=[

                         self.publish.year,self.publish.month,self.publish.day,
                         self.slug
                     ]

                       )

    class Meta:
        ordering=('-publish',)

    def __str__(self):
        return '{} by {}'.format(self.title,self.author)
class Comment(models.Model):
    post = models.ForeignKey(Post,models.CASCADE,related_name='comments',null=True,blank=True)
    body = models.TextField()
    name = models.CharField(max_length=80)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name,self.post)