from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse

class Post(models.Model):
    author= models.ForeignKey(User, on_delete=models.CASCADE)
    title= models.CharField(max_length=200)
    text= models.TextField()
    created_date= models.DateTimeField(default= timezone.now)
    publish_date= models.DateTimeField(blank= True, null=True)

    @property
    def publish(self):
        self.publish_date = timezone.now()
        self.save()
        
    @property
    def approve_comments(self):
        return self.comments.filter(approved_comment=True)
    
    def get_absolute_url(self):
        return reverse("post_detail", kwargs={'pk': self.pk})

    def __str__(self):
        return self.title



class Comment(models.Model):
    post= models.ForeignKey(Post, on_delete =models.CASCADE, related_name='comments')
    author= models.CharField(max_length=200)
    text=models.TextField()
    created_date=  models.DateTimeField(default=timezone.now)
    approved_comment= models.BooleanField(default=False)

    @property
    def approve(self):
        self.approved_comment= True
        self.save()
 

    def __str__(self):
        return self.text