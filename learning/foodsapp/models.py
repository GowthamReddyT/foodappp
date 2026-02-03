from django.db import models
from django.conf import settings
import uuid



class FoodItems(models.Model):
    CATEGORIES = [
        ("PIZZA", "Pizza"),
        ("BURGER", "Burger"),
        ("FRIES", "French Fries"),
        ("DESSERTS", "Desserts"),
        ("BEVERAGES", "Beverages"),
        ("BRIYANI", "Briyani"),
    ]

    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    rating = models.PositiveIntegerField()
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORIES)

    foodimg = models.ImageField(
        upload_to="foodimg/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class BaseOption(models.Model):
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    basetype = models.CharField(max_length=50)
    extra_price = models.PositiveIntegerField(default=0)


    image = models.ImageField(
        upload_to="base/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.basetype



class SizeOption(models.Model):
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    size_cm = models.DecimalField(max_digits=5, decimal_places=1)
    extra_price = models.PositiveIntegerField(default=0)

  
    image = models.ImageField(
        upload_to="size/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.size


class ToppingOption(models.Model):
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    toppingname = models.CharField(max_length=80)
    extra_price = models.PositiveIntegerField(default=0)


    image = models.ImageField(
        upload_to="topping/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.toppingname


class SauceOption(models.Model):
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    sausetype = models.CharField(max_length=80)
    extra_price = models.PositiveIntegerField(default=0)


    image = models.ImageField(
        upload_to="sauce/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.sausetype


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    extra_price = models.PositiveIntegerField(default=0)

    @property
    def total_price(self):
        return (self.food.price + self.extra_price) * self.quantity

    def __str__(self):
        return f"{self.user.username} - {self.food.name}"


class Order_Details(models.Model):
    order_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_quantity = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order_Details,
        on_delete=models.CASCADE,
        related_name="items"
    )
    food = models.ForeignKey(FoodItems, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()  

    def __str__(self):
        return f"{self.food.name} x {self.quantity}"
   