from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,HttpRequest
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from app.models import Product, Contact,Order,CustomUser
from django.contrib.auth import authenticate,login,logout
from datetime import datetime
from django.contrib import messages
import ast


# Create your views here.


def logIn(request):
    if request.method == "POST":
        loginusername = request.POST['loginuser']
        loginpassword = request.POST['loginpass']
        user = authenticate(username=loginusername,password=loginpassword,role="User")
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in successfully")
            return redirect("/home")
        else:
            messages.error(request,"Invalid login details")
            return redirect("/home")

def loGout(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect("/home")

def signup(request):
    all_users = CustomUser.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        flag = False
        if len(username) != 0 and len(first_name) != 0 and len(last_name) != 0 and len(email) != 0 and password == password_confirmation:
            for i in all_users:
                if i.email == email:
                    flag = True
            if flag == True:
                messages.warning(request,"The email has been already taken")
                return redirect("/home")
            else:
                    user = CustomUser.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password,email=email)
                    user.role = "User"
                    user.save()
                    messages.success(request,"Your account has been successfully created")
                    return redirect("/home")
        else:
             messages.warning(request,"Please fill the form correctly!")
             return redirect("/home")

def index(request):
    res = Product.objects.all()
    all_stocks  = []
    all_product_stocks = []
    for item in res:
           all_stocks.append(int(item.stock))
    for i,j in zip(res,all_stocks):
           all_product_stocks.append([i,j])
    if request.method == "POST":
        name = request.POST["username"]
        password = request.POST["password"]
        check_user = {'name': name, 'password': password}
        if User.objects.get(name=name, password=password):
            user = check_user
            return render(request, 'index.html', {'res': res,'all_stocks':all_product_stocks})
        else:
            return render(request, 'index.html', {'res': res,'all_stocks':all_product_stocks})
    else:
        return render(request, 'index.html', {'res': res,'all_stocks':all_product_stocks})


def about(request):
    return render(request, 'about.html')


def contact(request):
    if request.method == "POST":
        name = request.POST["name"]
        company_name = request.POST["company_name"]
        email = request.POST["email"]
        message = request.POST["messages"]
        if len(name) != 0 and len(company_name) != 0 and len(email) != 0 and len(message) != 0:
            contact = Contact(name=name, company_name=company_name,
                              email=email, message=message, date=datetime.today())
            contact.save()
            messages.success(request, 'We have received your message!')
            return render(request, 'contact.html')
        else:
            messages.warning(request, 'Please fill all the required info')
            return render(request, 'contact.html')
    return render(request, 'contact.html')


def pr_details(request, id):
    res = Product.objects.get(id=id)
    lst = []
    product_stock = int(res.stock)
    for i in range(1,product_stock+1):
        lst.append(i)
    return render(request, 'pr_details.html', {'x': res,'product_stock':product_stock,'lst':lst})


def cart(request, keys_str):
    if keys_str == "null":
        return render(request, 'cart.html', {'x': 0, 'total': 0, 'total_price_vat': 0})
    else:
    
        res = ast.literal_eval(keys_str)
        items = {'item': [], 'quantity': []}
        total_items = 0
        total_price = 0
        all_stocks = []
        all_cart_items = []
        for i in res.keys():
            pr = Product.objects.get(id=int(i))
            items['item'].append(pr)
        for j in res.values():
            items['quantity'].append(j)
        for m in items['quantity']:
            total_items = total_items + m
        for h in range(len(items['item'])):
            a = []
            m = items['item'][h]
            a.append(m)
            n = items['quantity'][h]
            a.append(n)
            all_cart_items.append(a)
        total_quantity = items['quantity']
        for i in range(len(total_quantity)):
            total_price = total_price + \
                (all_cart_items[i][0].price * total_quantity[i])
        for i in res.keys():
            pr = Product.objects.get(id=int(i))
            all_stocks.append(int(pr.stock))
        for i in range(len(all_cart_items)):
            all_cart_items[i].append(all_stocks[i])
        if total_price == 0:
            return render(request, 'cart.html', {'itm': all_cart_items, 'tq': total_quantity, 'total': total_items, 'total_price': total_price, 'total_price_vat': 0})

        return render(request, 'cart.html', {'itm': all_cart_items, 'tq': total_quantity, 'total': total_items, 'total_price': total_price, 'total_price_vat': (total_price+25),'all_stocks':all_stocks})


def cart_null(request):
    return render(request, 'cart.html', {'x': 0, 'total': 0})


def checkout(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobilenumber = request.POST['mobilenumber']
        address = request.POST['address']
        country = request.POST['hidec']
        state = request.POST['state']
        pincode = request.POST['pincode']
        payment = request.POST['hidep']
        u = User(name=name, mail_id=email, mobile_no=mobilenumber, address=address,
                 country=country, state=state, pincode=pincode, payment_method=payment)
        if u.save():
            return render(request, 'checkout.html', {'flag': 'yes'})
        else:
            return render(request, 'checkout.html', {'flag': 'no'})
    else:
        return render(request, 'checkout.html', {'flag': 'no'})


def checkout_buynow(request, id, quantity):
    return render(request, 'checkout_buynow.html', {'id': id, 'quantity': quantity})


def bill_buynow(request, id, quantity):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobilenumber = request.POST['mobilenumber']
        address = request.POST['address']
        country = request.POST['hidec']
        state = request.POST['state']
        pincode = request.POST['pincode']
        payment = request.POST['hidep']
        if len(name) != 0 and len(email) != 0 and len(mobilenumber) != 0 and len(address) != 0 and len(country) != 0 and len(state) != 0 and len(pincode) != 0 and len(payment) != 0:
            dct = {'name': name, 'email': email, 'mobilenumber': mobilenumber, 'address': address,
                   'country': country, 'state': state, 'pincode': pincode, 'payment': payment}
            p = Product.objects.get(id=id)
            return render(request, 'bill_buynow.html', {'info': dct, 'x': p, 'quantity': quantity, 'id': id})

        else:
            messages.warning(request, 'Please fill all the required info')
            return redirect("/checkout")


def bill(request, keys_str):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobilenumber = request.POST['mobilenumber']
        address = request.POST['address']
        country = request.POST['hidec']
        state = request.POST['state']
        pincode = request.POST['pincode']
        payment = request.POST['hidep']
        if len(name) != 0 and len(email) != 0 and len(mobilenumber) != 0 and len(address) != 0 and len(country) != 0 and len(state) != 0 and len(pincode) != 0 and len(payment) != 0:
            dct = {'name': name, 'email': email, 'mobilenumber': mobilenumber, 'address': address,
                   'country': country, 'state': state, 'pincode': pincode, 'payment': payment}
            res = ast.literal_eval(keys_str)
            items = {'item': [], 'quantity': []}
            total_items = 0
            total_price = 0
            all_cart_items = []
            for i in res.keys():
                pr = Product.objects.get(id=int(i))
                items['item'].append(pr)
            for j in res.values():
                items['quantity'].append(j)
            for m in items['quantity']:
                total_items = total_items + m
            for h in range(len(items['item'])):
                a = []
                m = items['item'][h]
                a.append(m)
                n = items['quantity'][h]
                a.append(n)
                all_cart_items.append(a)
            total_quantity = items['quantity']
            for i in range(len(total_quantity)):
                total_price = total_price + \
                    (all_cart_items[i][0].price * total_quantity[i])

            if total_price == 0:
                return render(request, 'bill.html', {'itm': all_cart_items, 'tq': total_quantity, 'total': total_items, 'total_price': total_price, 'total_price_vat': 0})

            return render(request, 'bill.html', {'itm': all_cart_items, 'tq': len(total_quantity), 'total': total_items, 'total_price': total_price, 'total_price_vat': (total_price+25), 'info': dct})

        else:
            messages.warning(request, 'Please fill all the required info')
            return redirect("/checkout")


def order(request, keys_str):
    if request.method == "POST":
        products_info = keys_str
        name = request.POST['name']
        email = request.POST['email']
        mobile_number = request.POST['mobile']
        address = request.POST['address']
        country = request.POST['country']
        state = request.POST['state']
        pincode = request.POST['pincode']
        payment_method = request.POST['payment']
        products = ""
        res = ast.literal_eval(keys_str)
        items = {'item': [], 'quantity': []}
        total_items = 0
        total_price = 0
        all_cart_items = []
        all_items = ""
        for key,value in res.items():
            product = Product.objects.get(id=int(key))
            if int(product.stock) == 0:
                messages.warning(request,'Sorry some item(s) may be out of stock!')
                return redirect('/home')
            else:
                product.stock = int(product.stock) - int(value)
                updated_stock = product.stock
                Product.objects.filter(id=int(key)).update(stock=updated_stock)
                for i in res.keys():
                    pr = Product.objects.get(id=int(i))
                    items['item'].append(pr)
                for j in res.values():
                    items['quantity'].append(j)
                for m in items['quantity']:
                    total_items = total_items + m
                for key,value in res.items():
                    all_items = all_items + " "+"Product_ID: "+str(key)+" "+"Quantity: "+str(value)+","
                for h in range(len(items['item'])):
                    a = []
                    m = items['item'][h]
                    a.append(m)
                    n = items['quantity'][h]
                    a.append(n)
                    all_cart_items.append(a)
                total_quantity = items['quantity']
                for i in range(len(total_quantity)):
                    total_price = total_price + \
                        (all_cart_items[i][0].price * total_quantity[i])
                order = Order(name=name, email=email, mobile_number=mobile_number, address=address, country=country, state=state,
                            pincode=pincode, payment_method=payment_method, product_ids=all_items, total_price=(total_price+25),order_str=keys_str)
                if order.save:
                    order.save()
                
                    return render(request, 'confirmation.html')
                else:
                    return render(request, 'error.html')


def order_buynow(request, id, quantity):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        mobile_number = request.POST['mobile']
        address = request.POST['address']
        country = request.POST['country']
        state = request.POST['state']
        pincode = request.POST['pincode']
        payment_method = request.POST['payment']
        product = Product.objects.get(id=int(id))
        if int(product.stock) == 0:
            messages.warning(request,'Sorry this item is out of stock')
            return redirect('/home')
        else:
            product.stock = int(product.stock) - int(quantity)
            updated_stock = product.stock
            Product.objects.filter(id=int(id)).update(stock=updated_stock)
            product = "Product-id: "+str(id) +" "+"Quantity: "+str(quantity)
            p = Product.objects.get(id=id)
            total_price = p.price + 25
            order = Order(name=name, email=email, mobile_number=mobile_number, address=address, country=country,
                        state=state, pincode=pincode, payment_method=payment_method, product_ids=product, total_price=total_price)
            if order.save:
                order.save()
                return render(request, 'confirmation.html')
            else:
                return render(request, 'error.html')


def admin_panel(request):
    user = CustomUser.objects.filter(role="User")
    return render(request, 'admin.html', {'user': user})

def admin_register(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']
        if len(username) != 0 and len(first_name) != 0 and len(last_name) != 0 and len(email) != 0 and password == password_confirmation:
            user = CustomUser.objects.create_user(username=username,first_name=first_name,last_name=last_name,password=password,email=email)
            user.role = "Admin"
            user.save()
            messages.success(request,"Your admin account has been successfully created")
            return redirect("/home")
        else:
             messages.warning(request,"Please fill the form correctly!")
             return redirect("/home")

def admin_login(request):
    if request.method == "POST":  
        loginusername = request.POST['loginuser']
        loginpassword = request.POST['loginpass']
        user = authenticate(username=loginusername,password=loginpassword,role="Admin")
        if user is not None:
            login(request,user)
            messages.success(request,"Logged in successfully")
            return redirect("/admin_panel")
        else:
            messages.error(request,"Invalid login details")
            return redirect("/home")


def all_products(request):
    products = Product.objects.all()
    return render(request,'all_products.html',{'products':products})

def all_users(request):
    user = CustomUser.objects.filter(role="Admin")
    return render(request,'all_users.html',{'user':user})


def product_edit(request,id):
    if request.method == "POST":
       image = request.POST['image']
       name = request.POST['name']
       description = request.POST['description']
       price = request.POST['price']
       stock = request.POST['stock']
       product = Product.objects.get(id=id)

       product.image = image
       product.name = name
       product.description = description
       product.price = price
       product.stock = stock

       product.save()
       products = Product.objects.all()
       return render(request,'all_products.html',{'products':products})

    else:
        product = Product.objects.get(id=id)
        return render(request,'products_edit.html',{'product':product})

def all_orders(request):
    orders = Order.objects.all()
    return render(request,'all_orders.html',{'orders':orders})


def order_delete(request,id):
    order = Order.objects.get(id=id)
    orders = ast.literal_eval(order.order_str)
    for i in orders.keys():
        pro_id = Product.objects.get(id=int(i))
        pro_id.stock = int(pro_id.stock) + orders[i]
        updated_stock = pro_id.stock
        Product.objects.filter(id=int(i)).update(stock=updated_stock)
    order.delete()
    messages.success(request,"Order has been cancelled successfully!")
    return redirect("/all_orders")



def add_products(request):
    if request.method == "POST":
      name = request.POST['name']
      image = request.POST['image']
      description = request.POST['description']
      price = request.POST['price']
      stock = request.POST['stock']
      product = Product(name=name,description=description,price=price,image=image,stock=stock)
      product.save()

      products = Product.objects.all()

      messages.success(request,"Product has been added successfully!")
      return render(request,'all_products.html',{'products':products})
 
    else:
        return render(request,'add_products.html')

def product_delete(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    products = Product.objects.all()
    messages.success(request,"Product has been deleted!")
    return render(request,'all_products.html',{'products':products})

def user_delete(request,id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    user = CustomUser.objects.all()
    messages.success(request,"User has been removed!")
    return render(request,'admin.html',{'user':user})


