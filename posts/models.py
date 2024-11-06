# from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User

class UserPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content_text = models.TextField(blank=True, null=True)
    content_file = models.FileField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
