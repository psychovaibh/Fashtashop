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
    path("re-payment/<int:id>/",views.repaymentpage,name="re-payment"),
    path('payment-success/<int:id>/<str:rppid>/<str:rpoid>/<str:rpsid>/', views.paymentSuccessPage,name="payment-success"),
    path("confirmation/<int:id>/",views.confirmationPage,name="confirmation"),
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