from django.contrib import admin
from django.urls import path,include
from app import views

urlpatterns = [
    path('home',views.index,name="home"),
    path("about",views.about,name="about"),
    path("contact",views.contact,name="contact"),
    path("pr_details/<int:id>",views.pr_details,name="pr_details"),
    path("home",views.index,name="home"),
    path("cart/<str:keys_str>",views.cart,name="cart"),
    path("checkout",views.checkout,name="checkout"),
    path("checkout_buynow/<int:id>/<int:quantity>",views.checkout_buynow,name="checkout_buynow"),
    path("bill/<str:keys_str>",views.bill,name="bill"),
    path("bill_buynow/<int:id>/<int:quantity>",views.bill_buynow,name="bill_buynow"),
    path("order/<str:keys_str>",views.order,name="order"),
    path("order_buynow/<int:id>/<int:quantity>",views.order_buynow,name="order_buynow"),
    path("admin_panel",views.admin_panel,name="admin_panel"),
    path("login",views.logIn,name="login"),
    path("signup",views.signup,name="signup"),
    path("logout",views.loGout,name="logout"),
    path("admin_register",views.admin_register,name='admin_register'),
    path("admin_login",views.admin_login,name='admin_login'),
    path("all_products",views.all_products,name='all_products'),
    path("all_users",views.all_users,name="all_users"),
    path("product/<int:id>",views.product_edit,name="product_edit"),
    path("all_orders",views.all_orders,name="all_orders"),
    path("all_orders/delete/<int:id>",views.order_delete,name="order_delete"),
    path("add_products",views.add_products,name="add_products"),
    path("product_delete/<int:id>",views.product_delete,name="product_delete"),
    path("user_delete/<int:id>",views.user_delete,name="user_delete"),
    
]
