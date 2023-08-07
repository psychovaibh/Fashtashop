from django.contrib import admin
from .models import *
# Register your models here.

# admin.site.register((maincategory,subcategory,brand,product,buyer,wishlist,billing,checkout,checkOutProduct,newslatter,contact))


@admin.register(maincategory)
class maincategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']

@admin.register(subcategory)
class subcategoryAdmin(admin.ModelAdmin):
    list_display=['id','name']

@admin.register(brand)
class brandAdmin(admin.ModelAdmin):
    list_display=['id','name','pic']

@admin.register(product)
class productAdmin(admin.ModelAdmin):
    list_display=['id','name','baseprice','discount','finalprice','stock','color','size','pic1','pic2','pic3','pic4']

@admin.register(buyer)
class buyerAdmin(admin.ModelAdmin):
    list_display=['id','name','username','email','phone','address','pin','city','state','pic']

@admin.register(wishlist)
class wishlistAdmin(admin.ModelAdmin):
    list_display=['id','product','buyer']

@admin.register(billing)
class billingAdmin(admin.ModelAdmin):
    list_display=['user','id','name','address','city','state','pin','phone','email']


@admin.register(checkout)
class checkoutAdmin(admin.ModelAdmin):
    list_display=['id','orderstatus','paymentstatus','paymentmode','subtotal','shipping','total','rppid','date','name','address','city','state','pin','phone','email']


@admin.register(checkOutProduct)
class checkOutProductAdmin(admin.ModelAdmin):
    list_display=['id','checkout','product','qty','total']


@admin.register(newslatter)
class newslatterAdmin(admin.ModelAdmin):
    list_display=['id','email']

@admin.register(contact)
class contactAdmin(admin.ModelAdmin):
    list_display=['id','name','email','message','status','date']