from django.test import TestCase
from .models import Product, Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Electronics',
            description='Electronic items'
        )

    def test_category_creation(self):
        self.assertEqual(self.category.name, 'Electronics')
        self.assertEqual(str(self.category), 'Electronics')


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Electronics')
        self.product = Product.objects.create(
            name='Laptop',
            description='Gaming laptop',
            price=999.99,
            category=self.category,
            stock=10
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Laptop')
        self.assertEqual(str(self.product), 'Laptop')
        self.assertTrue(self.product.in_stock)

    def test_product_out_of_stock(self):
        self.product.stock = 0
        self.assertFalse(self.product.in_stock)
