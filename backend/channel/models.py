from io import BytesIO
from django.db import models
from PIL import Image
from django.core.files import File
from django.db import models
from DjangoVueTest.settings import BASE_URL
from django.contrib.auth.models import User

class Channel(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = "Channels"
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'
    

class Channel_link(models.Model):
    channel_id = models.ForeignKey(Channel, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    

"""
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='category', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-date_added',)
    
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    
    def get_image(self):
        if self.image and hasattr(self.image, 'url'):
            return BASE_URL + self.image.url
        else: return ''

    def get_thumbnail(self):
        if self.thumbnail and hasattr(self.thumbnail, 'url'):
            return BASE_URL + self.thumbnail.url
        elif self.image and hasattr(self.image, 'url'):
            self.thumbnail = self.make_thumbnail(self.image)
            self.save()
            return BASE_URL + self.thumbnail.url
        else: return ''

    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail
"""