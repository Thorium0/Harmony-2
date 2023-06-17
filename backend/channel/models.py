from io import BytesIO
from django.db import models
from PIL import Image
from django.core.files import File
from django.db import models
from Harmony.settings import BASE_URL
from django.contrib.auth.models import User, Group


    
class Message(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='files/', blank=True, null=True)
