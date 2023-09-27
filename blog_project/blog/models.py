from django.db import models
from django.contrib.auth.models import User

import uuid
class BaseModel(models.Model):
    uid = models.UUIDField(primary_key=True , editable=False ,default=uuid.uuid4)
    class Meta:
        abstract = True

# Create your models here.

class BlogPost(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blogs')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs')
    created_at = models.DateField(auto_now=True)
    updated_at = models.DateField(auto_now=True)

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username