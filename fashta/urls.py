"""fashta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainApp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("",views.homePage,name="home"),
    path("shop/<str:mc>/<str:sc>/<str:br>/",views.shopPage,name="shop"),
    path("shopDetails/<int:id>/",views.shopDetailsPage,name="shopDetails"),
    path("addtocart/",views.addtocart,name="addtocart"),
    path("shoppingCart/",views.shoppingCartPage,name="shopping-cart"),
    path("deletefromcart/<str:id>/",views.deletecart),
    path("updatecart/<str:id>/<str:op>/",views.updatecart),
    path("checkOut/",views.checkOutPage,name="checkOut"),
    path("payment-success/",views.paymentSuccessPage,name="payment-success"),
    path("re-payment/<int:id>/",views.repayment,name="re-payment"),
    path("confirmation/",views.confirmationPage,name="confirmation"),
    path("about/",views.aboutPage,name="about_us"),
    path("contact/",views.contactPage,name="contact"),
    path("login/",views.loginPage,name="login"),
    path("signup/",views.signupPage,name="signup"),
    path("logout/",views.logoutView,name="logout"),
    path("profile/",views.profilePage,name="profile"),
    path("update-profile/",views.updateprofilePage,name="updateprofile"),
    path("wishlist/<int:id>/",views.mywishlist),
    path("delete-wishlist/<int:id>/",views.deletewishlist),
    path("newslatter-subscribe/",views.newslatterPage,name="newslatter-subscribe"),
    path("search/",views.search,name="search"),
    path("forget-password-1/",views.forgetpassword1,name="f-p-1"),
    path("forget-password-2/",views.forgetpassword2,name="f-p-2"),
    path("forget-password-3/",views.forgetpassword3,name="f-p-3"),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)