from django.db import models
from django.contrib.auth.models import User

class UserDetails(models.Model):

    user_type_choices = [
        ("USER", "User"),
        ("VENDOR", "Vendor"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone = models.BigIntegerField()
    address = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    userpic = models.ImageField(upload_to='userimg/', blank=True, null=True)

    user_type = models.CharField(
        max_length=100,
        choices=user_type_choices,
        default="USER"
    )

    def __str__(self):
        return self.user.username
