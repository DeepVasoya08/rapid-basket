from django.urls import path
from . import views

urlpatterns = [
    path("", views.store, name="store"),
    path("category/<str:slug>", views.productsView, name="products"),
    path("category/<str:cat_slug>/<str:pro_slug>", views.productDetails, name="product_details"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("signin/", views.signIn, name="signin"),
    path("signup/", views.signUp, name="signup"),
]
