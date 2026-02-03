from django.contrib import admin
from .models import (
    FoodItems,
    Order_Details,
    OrderItem,
    SizeOption,
    BaseOption,
    ToppingOption,
    SauceOption,
)

admin.site.register(FoodItems)
admin.site.register(SizeOption)
admin.site.register(BaseOption)
admin.site.register(ToppingOption)
admin.site.register(SauceOption)
admin.site.register(Order_Details)
admin.site.register(OrderItem)
