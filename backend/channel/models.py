from io import BytesIO
from django.db import models
from PIL import Image
from django.core.files import File
from django.db import models
from Harmony.settings import BASE_URL
from django.contrib.auth.models import User, Group


    
class Message(models.Model):
    Group = models.ForeignKey(Group, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='files/', blank=True, null=True)
