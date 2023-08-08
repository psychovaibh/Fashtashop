from django.shortcuts import render,HttpResponseRedirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.messages import success,error
from django.db.models import Q
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from fashta.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
import razorpay





def homePage(Request):
    products = product.objects.all().order_by("-id")[0:12]
    return render(Request,'index.html',{'products' : products})


def shopPage(Request,mc,sc,br,sort_by=None):
    # if(mc=="All" and sc=="All" and br=="All"):
    #     products = product.objects.all().order_by("-id")
    # elif(mc!="All" and sc=="All" and br=="All"):
    #     products = product.objects.filter(maincategoryproduct = maincategory.objects.get(name=mc)).order_by("-id")
    # elif(mc=="All" and sc!="All" and br=="All"):
    #     products = product.objects.filter(subcategoryproduct = subcategory.objects.get(name=sc)).order_by("-id")
    # elif(mc=="All" and sc=="All" and br!="All"):
    #     products = product.objects.filter(brandproduct = brand.objects.get(name=br)).order_by("-id")
    # elif(mc!="All" and sc!="All" and br=="All"):
    #     products = product.objects.filter(maincategoryproduct = maincategory.objects.get(name=mc), subcategoryproduct = subcategory.objects.get(name=sc)).order_by("-id")
    # elif(mc=="All" and sc!="All" and br!="All"):
    #     products = product.objects.filter(subcategoryproduct = subcategory.objects.get(name=sc), brandproduct = brand.objects.get(name=br)).order_by("-id")
    # elif(mc!="All" and sc=="All" and br!="All"):
    #     products = product.objects.filter(maincategoryproduct = maincategory.objects.get(name=mc), brandproduct = brand.objects.get(name=br)).order_by("-id")
    # else:
    #     products = product.objects.filter(maincategoryproduct = maincategory.objects.get(name=mc), subcategoryproduct = subcategory.objects.get(name=sc), brandproduct = brand.objects.get(name=br)).order_by("-id")
    

    sort_by = Request.GET.get("sort_by")

    query = Q()
    if mc !="All":
        query &= Q(maincategoryproduct__name = mc)
    if sc !="All":
        query &= Q(subcategoryproduct__name = sc)
    if br !="All":
        query &= Q(brandproduct__name = br) 
    
    products = product.objects.filter(query)

    if sort_by == "low_to_high":
        products = products.order_by("finalprice")
    elif sort_by == "high_to_low":
        products = products.order_by("-finalprice")
    elif sort_by == "latest_first":
        products = products.order_by("-id")

    maincategorys = maincategory.objects.all().order_by("id")
    subcategorys = subcategory.objects.all().order_by("-id")
    brands = brand.objects.all().order_by("id")
    return render(Request,'shop.html',{'products': products, 'maincategorys': maincategorys, 'subcategorys' : subcategorys, 'brands' : brands, 'mc' : mc, 'sc' : sc, 'br' : br})


def shopDetailsPage(Request,id):
    products = product.objects.get(id=id)
    return render(Request,'shop-details.html',{'products':products})


def addtocart(Request):
    if(Request.method=="POST"):
        cart = Request.session.get('cart',None)
        qty = int(Request.POST.get("qty"))
        id = Request.POST.get("id")
        try:
            p = product.objects.get(id=id)
            if(cart):
                if(str(id) in cart.keys()):
                    item = cart[str(id)]
                    item['qty'] = item['qty'] + qty
                    item['total'] = item['total'] + (qty * item['price'])
                    cart[str(id)] = item
                else:
                    cart.setdefault(str(id),
                    {'productid':id,'name':p.name,'brand':p.brandproduct.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':qty,'total':qty*p.finalprice,'pic':p.pic1.url})
            else:
                cart = {str(id):{'productid':id,'name':p.name,'brand':p.brandproduct.name,'color':p.color,'size':p.size,'price':p.finalprice,'qty':qty,'total':qty*p.finalprice,'pic':p.pic1.url}}

            Request.session['cart'] = cart
        except:
            pass
    return HttpResponseRedirect("/shoppingCart/")

def shoppingCartPage(Request):
    cart = Request.session.get('cart',None)
    subtotal = 0
    shipping = 0
    total = 0
    if(cart):
        for value in cart.values():
            subtotal = subtotal + value['total']
        if(subtotal>0 and subtotal<1000):
            shipping = 130
        else:
            shipping = 0
        total = subtotal + shipping
    return render(Request,'shopping-cart.html',{'cart':cart,'subtotal':subtotal,'shipping':shipping,'total':total})

def deletecart(Request,id):
    cart = Request.session.get("cart",None)
    if(cart):
        del cart[id]
        Request.session['cart'] = cart
    else:
        pass
    return HttpResponseRedirect("/shoppingCart/")


def updatecart(Request,id,op):
    cart = Request.session.get("cart",None)
    if(cart):
        item = cart[id]
        if(op=='dec' and item['qty']==1):
            return HttpResponseRedirect("/shoppingCart/")
        else:
            if(op=='dec'):
                item['qty'] = item['qty'] -1
                item['total'] = item['total'] - item['price']
            else:
                item['qty'] = item['qty'] +1
                item['total'] = item['total'] + item['price']
        cart[id] = item
        Request.session['cart'] = cart
    else:
        pass
    return HttpResponseRedirect("/shoppingCart/")



def aboutPage(Request):
    return render(Request,'about.html')


def contactPage(Request):
    if(Request.method=="POST"):
        name = Request.POST.get("name")
        email = Request.POST.get("email")
        message = Request.POST.get("message")

        c = contact()
        c.name = name
        c.email = email
        c.message = message
        try:
            c.save()
            success(Request,"Your Message has been received Succesfully!")
        except:
            error(Request,"Some error occured!")
        return HttpResponseRedirect("/contact/")
    return render(Request,'contact.html')


def loginPage(Request):
    if(Request.method=="POST"):
        username = Request.POST.get("username")
        password = Request.POST.get("password")
        user = authenticate(username = username, password = password)
        if(user is not None):
            login(Request,user)
            if(user.is_superuser):
                return HttpResponseRedirect("/admin/")
            else:
                return HttpResponseRedirect("/profile/")
        else:
            error(Request,"Invalid Username or Password!!")
    return render(Request,'login.html')


def signupPage(Request):
    if(Request.method=="POST"):
        password = Request.POST.get("password")
        cpassword = Request.POST.get("cpassword")
        if(password == cpassword):
            name = Request.POST.get("name")
            username = Request.POST.get("username")
            email = Request.POST.get("email")
            phone = Request.POST.get("phone")

            try:
                User.objects.create_user(username = username, email = email, password = password, first_name = name)

                b = buyer()
                b.name = name
                b.email = email
                b.username = username
                b.phone = phone
                b.save()
                return HttpResponseRedirect("/login/")
            except:
                error(Request,"Username Already Taken!!!")
        else:
            error(Request,"Password and Confirm Password doesn't match!")
    return render(Request,'signup.html')

@login_required(login_url="/login/")
def logoutView(Request):
    logout(Request)
    return HttpResponseRedirect("/")


@login_required(login_url="/login/")
def profilePage(Request):
    if(Request.user.is_superuser):
        return HttpResponseRedirect("/admin/")
    username = Request.user.username
    try:
        buyerdata = buyer.objects.get(username = username)
        mywishlist = wishlist.objects.filter(buyer = buyerdata)

        co = checkout.objects.filter(buyer=buyerdata)
        orders = []
        for item in co:
            cp = checkOutProduct.objects.filter(checkout=item)
            orders.append({'co':item,'cp':cp})
        return render(Request,"profile.html",{"buyerdata" : buyerdata,'wishlist' : mywishlist,'order':orders })
    except:
        return HttpResponseRedirect("/login/")
    

@login_required(login_url="/login/")
def updateprofilePage(Request):
    if(Request.user.is_superuser):
        return HttpResponseRedirect("/admin/")
    username = Request.user.username
    try:
        buyerdata = buyer.objects.get(username=username)
        if(Request.method=="POST"):
            buyerdata.name = Request.POST.get("name")
            buyerdata.email = Request.POST.get("email")
            buyerdata.phone = Request.POST.get("phone")
            buyerdata.city = Request.POST.get("city")
            buyerdata.state = Request.POST.get("state")
            buyerdata.pin = Request.POST.get("pin")
            buyerdata.address = Request.POST.get("address")
            if(Request.FILES.get("pic")):
                buyerdata.pic = Request.FILES.get("pic")
            buyerdata.save()
            return HttpResponseRedirect("/profile/")
        return render(Request,"update-profile.html",{"buyer": buyerdata})
    except:
        return HttpResponseRedirect("/login/")
    

@login_required(login_url="/login/")
def mywishlist(Request,id):
    try:
        buyerproduct = buyer.objects.get(username = Request.user.username)
        products = product.objects.get(id=id)
        try:
            w = wishlist.objects.get(product=products,buyer=buyerproduct)
        except:
            w = wishlist()
            w.product = products
            w.buyer = buyerproduct
            w.save()
    except:
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def deletewishlist(Request,id):
    try:
        products = wishlist.objects.get(id=id)
        products.delete()
    except:
        pass
    return HttpResponseRedirect("/profile/")



client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY,settings.RAZORPAY_API_SECRET_KEY))
@login_required(login_url="/login/")
def checkOutPage(Request):
    if(Request.user.is_superuser):
        return HttpResponseRedirect("/admin/")
    
    Buyer = buyer.objects.get(username = Request.user.username)
    form_type = Request.POST.get("form_type")
    subtotal = 0 
    shipping = 0
    total = 0
    cart = Request.session.get('cart',None)
    if(cart):
        for value in cart.values():
            subtotal = subtotal + value['total']
        if(subtotal>0 and subtotal<1000):
            shipping = 130
        else:
            shipping = 0
        total = subtotal + shipping
    else:
        HttpResponseRedirect("/shoppingCart/")
    try:
        billing_user = billing.objects.filter(user=Request.user)
    except billing.DoesNotExist:
        billing_user = None


    if(Request.method == "POST"):
        if(form_type == "type_1"):
            name = Request.POST.get("name")
            address = Request.POST.get("address")
            user = Request.user
            city = Request.POST.get("city")
            state = Request.POST.get("state")
            pin = Request.POST.get("pin")
            phone = Request.POST.get("phone")
            email = Request.POST.get("email")


            b = billing()
            b.user = user
            b.name = name
            b.address = address
            b.city = city
            b.state = state
            b.pin = pin
            b.phone = phone
            b.email = email
            b.save()


        elif(form_type=="type_2"):
            mode = Request.POST.get("mode")
            selected_address_id = Request.POST.get("selected_address")
            selected_address = billing.objects.get(id=selected_address_id)
            co = checkout()
            co.buyer = Buyer
            co.subtotal = subtotal
            co.total = total
            co.shipping = shipping

            co.name = selected_address.name
            co.address = selected_address.address
            co.city = selected_address.city
            co.state = selected_address.state
            co.pin = selected_address.pin
            co.phone = selected_address.phone
            co.email = selected_address.email 
            co.save()

            for key,value in cart.items():
                p = product.objects.get(id = int(key))
                cp = checkOutProduct()

                cp.checkout = co
                cp.product = p
                cp.qty = value['qty']
                cp.total = value['total']
                cp.save()
                Request.session['cart'] = {}

            if(mode=="COD"):
                return HttpResponseRedirect("/confirmation/"+str(co.id)+"/")
            else:
                orderAmount = co.total*100
                orderCurrency = "INR"
                paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
                paymentId = paymentOrder['id']
                co.paymentmode=1
                co.save()
                return render(Request,"pay.html",{
                    "amount":orderAmount,
                    "displayAmount":co.total,
                    "api_key":settings.RAZORPAY_API_KEY,
                    "order_id":paymentId,
                    "User":Buyer,
                    "id":co.id
                })
        

    return render(Request, 'checkout.html', {'bill': billing_user,'total':total,'subtotal':subtotal,'shipping':shipping,'cart':cart,'buyer':Buyer})


@login_required(login_url='/login/')
def repaymentpage(Request,id):
    try:
        co = checkout.objects.get(id=id)
        Buyer = buyer.objects.get(username=Request.user.username)
        orderAmount = co.total*100
        orderCurrency = "INR"
        paymentOrder = client.order.create(dict(amount=orderAmount,currency=orderCurrency,payment_capture=1))
        paymentId = paymentOrder['id']
        co.paymentmode=1
        co.save()
        return render(Request,"pay.html",{
                "amount":orderAmount,
                "displayAmount":co.total,
                "api_key":settings.RAZORPAY_API_KEY,
                "order_id":paymentId,
                "User":Buyer,
                "id":id
                })
    except:
        return HttpResponseRedirect("/profile/")


@login_required(login_url="/login/")
def paymentSuccessPage(Request,id,rppid,rpoid,rpsid):
    check = checkout.objects.get(id=id)
    check.rppid=rppid
    check.paymentstatus=1
    check.save()
    print(id)
    return HttpResponseRedirect('/confirmation/'+str(id)+"/")


@login_required(login_url="/login/")
def confirmationPage(Request,id):
    try:
        Buyer = buyer.objects.get(username=Request.user.username)
        co = checkout.objects.get(id=id)
        cart = checkOutProduct.objects.filter(checkout=co)
        subtotal = 0
        shipping = 0
        total = 0
        for item in cart:
            subtotal = subtotal + item.total
        if(subtotal>0 and subtotal<1000):
            shipping = 150
        total = subtotal+shipping
    
        return render(Request,"confirmation.html",{'cart':cart,'subtotal':subtotal,'shipping':shipping,'total':total,'buyer':Buyer,'checkout':co})
    except:
        return HttpResponseRedirect("/admin/")
    


def newslatterPage(Request):
    if(Request.method=="POST"):
        email = Request.POST.get("email")
        n = newslatter()
        n.email = email
        try:
            n.save()
            success(Request,"Thanks for Subscribe.")
        except:
            error(Request,"Your Email is already subscribed!")
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")
    

def search(Request):
    if(Request.method=="POST"):
        search = Request.POST.get("search")
        try:
            maincat = maincategory.objects.get(name=search)
        except:
            maincat = None
        try:
            subcat = subcategory.objects.get(name=search)
        except:
            subcat = None
        try:
            bra = brand.objects.get(name=search)
        except:
            bra = None

        products = product.objects.filter(Q(name__icontains=search)|Q(maincategoryproduct=maincat)|Q(subcategoryproduct=subcat)|Q(brandproduct=bra)|Q(color=search)|Q(description__icontains=search))
        
        maincat_list = maincategory.objects.all().order_by("-id")
        subcat_list = subcategory.objects.all().order_by("-id")
        bra_list = brand.objects.all().order_by("-id")
        return render(Request,"shop.html",
            {'products':products,'maincategory':maincat_list,'subcategory':subcat_list,'brand':bra_list,'mc':"All",'sc':"All",'br':"All"})
    else:
        return HttpResponseRedirect('/')


def forgetpassword1(Request):
    if(Request.method=="POST"):
        user = Request.POST.get("username")
        try:
            buyeruser = buyer.objects.get(username=user)
            otp = randint(100000,999999)
            buyeruser.otp = otp
            buyeruser.save()


            subject = "Forget Password Don't Worry We Can Recover Your Password! "
            message = f'''
                    Hi {buyeruser.name}, Your OTP is {otp}
                    For Security Do not share your otp to anyone!
                    Your Security is our concern.
                    Fashta-Shop
                    '''

            email_from = settings.EMAIL_HOST_USER
            recipient_list = [buyeruser.email, ]
            send_mail( subject, message, email_from, recipient_list )
            Request.session['reset-password-user'] = buyeruser.username
            success(Request,"OTP send successfully!")
            return HttpResponseRedirect("/forget-password-2/")
        except:
            error(Request,"Username Not Found In Our Database!!!")
    return render(Request,"forgetpassword1.html")


def forgetpassword2(Request):
    username = Request.session.get("reset-password-user")
    if(Request.method=="POST"):
        otp = int(Request.POST.get("otp"))
        buyeruser = buyer.objects.get(username=username)
        if(otp==buyeruser.otp):
            return HttpResponseRedirect("/forget-password-3/")
        else:
            error(Request,'Invalid OTP')
    if username:
        return render(Request,'forgetpassword2.html')
    else:
        return HttpResponseRedirect("/forget-password-1/")


def forgetpassword3(Request):
    username = Request.session.get("reset-password-user")
    if(Request.method=="POST"):
        password = Request.POST.get("password")
        cpassword = Request.POST.get("cpassword")
        if(password==cpassword):
            user = User.objects.get(username=username)
            user.set_password(password)
            user.save()
            del Request.session['reset-password-user']
            return HttpResponseRedirect("/login/")
        else:
            error(Request,"Password don't metched please check password!")
    if username:
        return render(Request,'forgetpassword3.html')
    else:
        return HttpResponseRedirect("/forget-password-1/")