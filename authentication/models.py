from django.db import models

class Product(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.title

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": float(self.price),
            "image": self.image.url
        }

from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class SavedDesign(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    design_image = models.TextField()  # store base64 PNG data URL
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

class Design(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='designs/')
    name = models.CharField(max_length=100, default='My Design')
    created_at = models.DateTimeField(auto_now_add=True)
from django.db import models

class Order(models.Model):
    name = models.CharField(max_length=255)
    total = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.name} - ₹{self.total}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.IntegerField()
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    # image = models.URLField(blank=True, null=True)
    image = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} x {self.title} (Order {self.order.id})"
