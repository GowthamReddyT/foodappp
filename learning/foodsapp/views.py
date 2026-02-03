from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from learningapp.models import UserDetails
from foodsapp.utils import send_email_view
from .models import (
    FoodItems,
    BaseOption,
    SizeOption,
    ToppingOption,
    SauceOption,
    Cart,
    Order_Details,
    OrderItem,
)


def allfoods(request):
    foods = FoodItems.objects.all()
    return render(request, "foods/allfoods.html", {
        "allfooditem": foods
    })


@login_required
def Food_details(request, id):
    food = get_object_or_404(FoodItems, id=id)
    return render(request, "foods/foodDetails.html", {
        "fooditems": food
    })


@login_required
def customize_food(request, id):
    food = get_object_or_404(FoodItems, id=id)

    base_options = BaseOption.objects.filter(food=food)
    size_options = SizeOption.objects.filter(food=food)
    topping_options = ToppingOption.objects.filter(food=food)
    sauce_options = SauceOption.objects.filter(food=food)

    if request.method == "POST":
        extra = 0

        if request.POST.get("base"):
            extra += BaseOption.objects.get(id=request.POST["base"]).extra_price

        if request.POST.get("size"):
            extra += SizeOption.objects.get(id=request.POST["size"]).extra_price

        if request.POST.get("topping"):
            extra += ToppingOption.objects.get(id=request.POST["topping"]).extra_price

        if request.POST.get("sauce"):
            extra += SauceOption.objects.get(id=request.POST["sauce"]).extra_price

        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            food=food
        )

        cart_item.extra_price = extra

        if not created:
            cart_item.quantity += 1

        cart_item.save()
        return redirect("foodsapp:cart")

    return render(request, "foods/customize.html", {
        "food": food,
        "base_options": base_options,
        "size_options": size_options,
        "topping_options": topping_options,
        "sauce_options": sauce_options,
    })



@login_required
def addFood(request):
    if request.method == "POST":
        FoodItems.objects.create(
            name=request.POST.get("name"),
            price=request.POST.get("price") or 0,
            rating=request.POST.get("rating") or 0,
            category=request.POST.get("category"),
            description=request.POST.get("description"),
            foodimg=request.FILES.get("foodimg"),
        )
        return redirect("foodsapp:allfoods")

    return render(request, "foods/addfood.html")


@login_required
def add_to_cart(request, id):
    food = get_object_or_404(FoodItems, id=id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food=food
    )
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect("foodsapp:cart")


@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in cart_items)
    return render(request, "foods/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price
    })


@login_required
def update_cart(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    if request.method == "POST":
        item.quantity = int(request.POST.get("quantity", 1))
        item.save()
    return redirect("foodsapp:cart")


@login_required
def remove_cart_item(request, id):
    item = get_object_or_404(Cart, id=id, user=request.user)
    item.delete()
    return redirect("foodsapp:cart")


from learningapp.models import UserDetails

@login_required
def order_details(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect("foodsapp:cart")

    total_quantity = sum(i.quantity for i in cart_items)
    total_amount = sum(i.total_price for i in cart_items)

    # FETCH USER ADDRESS (IMPORTANT)
    user_details = UserDetails.objects.filter(user=request.user).first()

    address = (
        f"{user_details.address}, {user_details.street}, "
        f"{user_details.city} - {user_details.zipcode}"
        if user_details else "Address not available"
    )

    if request.method == "POST":
        # SAVE ORDER FIRST
        order = Order_Details.objects.create(
            user=request.user,
            total_quantity=total_quantity,
            total_amount=total_amount
        )

        #  SAVE ORDER ITEMS
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                food=item.food,
                quantity=item.quantity,
                price=item.food.price + item.extra_price
            )   

      
        return render(request, "foods/order.html", {
            "order": order,
            "address": address,
        })

    return render(request, "foods/payment.html", {
        "cart_items": cart_items,
        "total_price": total_amount,
        "preview": True,
    })

@login_required
def payment(request):
    order = Order_Details.objects.filter(user=request.user).last()

    if not order:
        return redirect("foodsapp:cart")

    user_details = UserDetails.objects.filter(user=request.user).first()

    address = (
        f"{user_details.address}, {user_details.street}, "
        f"{user_details.city} - {user_details.zipcode}"
        if user_details else "Address not available"
    )

    # SEND EMAIL WITH CONTEXT
    send_email_view(
        email=request.user.email,
        user=request.user,
        order=order,
        address=address
    )

    # CLEAR CART AFTER PAYMENT
    Cart.objects.filter(user=request.user).delete()

    return render(request, "foods/payment.html", {
        "order": order,
        "address": address,
    })