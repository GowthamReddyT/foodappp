from django.urls import path
from . import views

app_name = "foodsapp"

urlpatterns = [
    path("allfoods/", views.allfoods, name="allfoods"),
    path("food/<int:id>/", views.Food_details, name="food_details"),
    path("food/<int:id>/customize/", views.customize_food, name="customizeFood"),

    path("addfood/", views.addFood, name="addfood"),
    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),

    path("cart/", views.cart, name="cart"),
    path("cart/update/<int:id>/", views.update_cart, name="update_cart"),
    path("cart/remove/<int:id>/", views.remove_cart_item, name="remove_cart_item"),

    path("order/", views.order_details, name="order"),
    path("payment/", views.payment, name="payment"),
   

]
