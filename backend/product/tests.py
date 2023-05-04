from django.test import TestCase

from tempfile import NamedTemporaryFile
from DjangoVueTest.settings import MEDIA_URL, BASE_URL
import os

from .models import Product, Category

class CategoryTestCase(TestCase):
    def setUp(self):
        Category.objects.create(name="Test Category", slug="test-category")
    

class ProductTestCase(TestCase):
    category = None
    testImage = None

    def setUp(self):
        self.category = Category.objects.create(name="Test Category", slug="test-category")
        self.testImage = NamedTemporaryFile(suffix=".jpg", delete=True)
        Product.objects.create(
            name="Test Product",
            slug="test-product",
            price=100,
            category=self.category,
            image=self.testImage.name
        )

    def test_product(self):
        product = Product.objects.get(slug="test-product")
        self.assertEqual(product.price, 100)
        self.assertEqual(product.category.name, "Test Category")
        self.assertEqual(product.get_absolute_url(), "/test-category/test-product/")
        #test = self.testImage.name.strip("/")
        #print(test)
        filePath = os.path.join(BASE_URL+"/", MEDIA_URL, self.testImage.name.strip("/"))
        #print(filePath)
        self.assertEqual(product.get_image(), filePath)
        self.assertEqual(product.get_thumbnail(), filePath)

