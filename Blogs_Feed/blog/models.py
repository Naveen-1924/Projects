from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title=models.CharField(max_length=100)
    content=models.TextField()
    date_posted=models.DateTimeField(default=timezone.now)
    #default =timezone.now is for if the post is edited then
    #time will also updated automatically
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    ##is user got deleted then his posts will delete automatically

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail',kwargs={'pk':self.pk})
    
    
    
