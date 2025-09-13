from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   path('', views.index, name="index"),
   path('signup/', views.signup, name="signup"),
   path('signin/', views.signin, name="signin"),
   path('signout/', views.signout, name="signout"),
   path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('api/chat/', views.chat_api, name='chat_api'),
    path('products/', views.products, name='products'),
    path('products/cart/', views.cart_view, name='cart'),
    path('save_design/', views.save_design, name='save_design'),
    path('outfit_builder/', views.outfit_builder, name='outfit_builder'),
    path("get-outfit-image/", views.get_outfit_image, name="get_outfit_image"),

    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('my-designs/', views.my_designs, name='my_designs'),
      path('recommender/', views.recommender, name='simple_fashion_recommender'),
      path('place_order/', views.place_order, name='place_order'),
    path('order_success/', views.order_success, name='order_success'),
    path("get-products/", views.get_products, name="get-products"),
]

