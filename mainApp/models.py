from django.db import models
from django.contrib.auth.models import User

class maincategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return str(self.id) + " " + self.name
    


class subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,unique=True)

    def __str__(self):
        return str(self.id) + " " + self.name

    

class brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30,unique=True)
    pic = models.ImageField(upload_to="uploads/brand")

    def __str__(self):
        return str(self.id) + " " + self.name 

    
class product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    maincategoryproduct = models.ForeignKey(maincategory,on_delete=models.CASCADE)
    subcategoryproduct = models.ForeignKey(subcategory,on_delete=models.CASCADE)
    brandproduct = models.ForeignKey(brand,on_delete=models.CASCADE)
    baseprice = models.IntegerField()
    discount = models.IntegerField()
    finalprice = models.IntegerField()
    stock = models.BooleanField(default=True)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    description = models.TextField(default="This is Sample Product")
    pic1 = models.ImageField(upload_to="uploads/product")
    pic2 = models.ImageField(upload_to="uploads/product",default=None,blank=True,null=True)
    pic3 = models.ImageField(upload_to="uploads/product",default=None,blank=True,null=True)
    pic4 = models.ImageField(upload_to="uploads/product",default=None,blank=True,null=True)


    def __str__(self):
        return str(self.id) + " " + self.name
    

class buyer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=30,unique=True)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=15,default="")
    address = models.TextField(default="",null=True,blank=True)
    pin = models.IntegerField(default=None,null=True,blank=True)
    city = models.CharField(max_length=30,default="",null=True,blank=True)
    state = models.CharField(max_length=30,default="",null=True,blank=True)
    pic = models.ImageField(upload_to="uploads/users", default="" ,blank=True,null=True)
    otp = models.IntegerField(default=None,blank=True,null=True)

    def __str__(self):
        return str(self.id) + " " + self.name + " " + self.username


class wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    buyer = models.ForeignKey(buyer,on_delete=models.CASCADE)

    def __str_(self):
        return str(self.id)+ " "+ self.product +" "+ self.buyer.username
    

class billing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=60)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    pin = models.IntegerField()
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=40)

    def __str__(self):
        return str(self.id) + " " + self.name + " " + self.address
    

orderStatusOptions = (
    (0,"Order is Placed"),
    (1,"Order is Packed"),
    (2,"Ready to Dispatch"),
    (3,"Dispatched"),
    (4,"Out For Delivery"),
    (5,"Delivered"))
paymentStatusOptions = (
    (0,"Pending"),
    (1,"Done"))
paymentModeOptions = (
    (0,"COD"),
    (1,"NetBanking"))

class checkout(models.Model):
    id= models.AutoField(primary_key=True)
    buyer = models.ForeignKey(buyer,on_delete=models.CASCADE)
    orderstatus = models.IntegerField(choices=orderStatusOptions,default=0)
    paymentstatus = models.IntegerField(choices=paymentStatusOptions,default=0)
    paymentmode = models.IntegerField(choices=paymentModeOptions,default=0)
    subtotal = models.IntegerField()
    shipping = models.IntegerField()
    total = models.IntegerField()
    rppid = models.CharField(max_length=20,default="",null=True,blank=True)
    date = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=100,default="")
    address = models.CharField(max_length=200,default="")
    city = models.CharField(max_length=100,default="")
    state = models.CharField(max_length=100,default="")
    pin = models.CharField(max_length=10,default="")
    phone = models.CharField(max_length=15,default="")
    email = models.EmailField(max_length=100,default="")


    def __str__(self):
        return str(self.id) + " " + self.buyer.username
    
class checkOutProduct(models.Model):
    id = models.AutoField(primary_key=True)
    checkout = models.ForeignKey(checkout,on_delete=models.CASCADE)
    product = models.ForeignKey(product,on_delete=models.CASCADE)
    qty = models.IntegerField()
    total = models.IntegerField()


    def __str__(self):
        return str(self.id)


class newslatter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True,max_length=50)

    def __str__(self):
        return str(self.id) + " / " + self.email

class contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    message = models.TextField()
    status = models.BooleanField(default=True)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id) + " / " + self.email