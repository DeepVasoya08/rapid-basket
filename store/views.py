from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
import json
import datetime

from .models import *
from .utils import cartCookie, cartData, guestCheckout
from .form import CreateUserForm


user = ""
email = ""


def store(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    categories = Category.objects.all()

    context = {"categories": categories, "cartItems": cartItems}
    return render(request, "store/store.html", context)


def cart(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": False,
    }
    return render(request, "store/cart.html", context)


def checkout(request):
    data = cartData(request)
    cartItems = data["cartItems"]
    order = data["order"]
    items = data["items"]

    context = {
        "items": items,
        "order": order,
        "cartItems": cartItems,
        "shipping": False,
    }
    return render(request, "store/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    # print("action: ", action)
    # print("productId", productId)

    customer = request.user.customer

    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item Added", safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        # print("user not logged in")
        customer, order = guestCheckout(request, data)

    total = float(data["form"]["total"])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data["shipping"]["address"],
            city=data["shipping"]["city"],
            state=data["shipping"]["state"],
            zipcode=data["shipping"]["zipcode"],
        )

    return JsonResponse("Payment complete", safe=False)


def signUp(request):
    global user, email
    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            superuser = User.objects.filter(username=user)
            # customer, created = Customer.objects.get_or_create(
            #     user=User, name=user, email=email
            # )
            # customer.save()

            messages.success(request, "Account created")
            return redirect("signin")

    context = {"form": form}

    return render(request, "store/signup.html", context)


def signIn(request):
    global user, email

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # user = form.cleaned_data.get("username")
        # email = form.cleaned_data.get("email")

        auth_user = authenticate(username=username, password=password)

        if auth_user is not None:
            login(request, auth_user)
            customer, created = Customer.objects.get_or_create(
                user=request.user, name=user, email=email
            )
            customer.save()
            return redirect("store")
        else:
            messages.error(request, "invalid username/password")
            return redirect("store")

    return render(request, "store/signin.html")


def signOut(request):
    pass
