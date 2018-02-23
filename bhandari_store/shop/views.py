from django.shortcuts import render, redirect
from .models import Product, Cart, Transaction
import datetime
from django.db.models import Sum
import os
import random
from .forms import ProductForm, UpdatenameForm, PriceForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
# Create your views here.
def home(request):
    if request.user.is_superuser:
        # get the products id
        try:
            # get from search bar
            query = request.GET.get('q')
            if query:
                products = Product.objects.filter(name__icontains=query)

                context = {
                    'products': products,
                    'query': query
                }
                return render(request, 'shop/search.html', context)

            # other main
            pid = request.GET.get('product_id')
            product = Product.objects.get(id=pid)
            carts = Cart.objects.all()
            total = Cart.objects.aggregate(Sum('amount'))['amount__sum']


            if request.method == 'POST':
                # get contents of that item
                name = product.name
                quantity = request.POST.get('qt')
                if int(quantity) > int(product.stocks):
                    error = "There are  " + str(product.stocks) + " items in the stock"
                else:
                    amount = int(product.selling_price) * int(quantity)
                    
                    cart = Cart(product=product, quantity=quantity, amount=amount)
                    
                    decrased_stock = int(product.stocks) - int(quantity)
                    product.stocks = decrased_stock
                    product.left_amount = int(product.left_amount) - int(quantity) * int(product.cost_price)
                    product.save()
                    # add to the transaction
                    pl = float(product.selling_price)*float(quantity) - float(product.cost_price) * float(quantity)
                    dt = datetime.datetime.now().date()
                    if pl < 0:
                        remark = 'Loss'
                    else:
                        remark = 'Profit'
                    # add to cart
                    cart.save()
                    tr = Transaction(product=product, selling_price=product.selling_price, profit_or_loss=pl, sold_on=dt,remark=remark, total_amount=amount, quantity=quantity, cart_id=cart.id )
                    tr.save()
                    carts = Cart.objects.all()

                    total = Cart.objects.aggregate(Sum('amount'))
            context = {
                'product': product,
                'carts': carts,
                'total': total,
            }

            return render(request, 'shop/index.html', context)
        except:
            error = 'Invalid Input. Please Try Again'
            carts = Cart.objects.all()
            total = Cart.objects.aggregate(Sum('amount'))['amount__sum']
            return render(request, 'shop/index.html', {'carts': carts, 'total':total, 'error': error})
    else:
        return redirect("shop:login_user")

# add products to the database
def add_products(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            # get items
            name = request.POST.get('name')
            stocks = request.POST.get('stocks')
            cp = request.POST.get('cp')
            sp = request.POST.get('sp')
            totalcp = float(stocks) * float(cp)
            totalsp = int(stocks) * int(sp)
            edate = request.POST.get('edate')
            added_date = datetime.datetime.now().date()
            left_amount = totalcp
            assumed_profit = float(totalsp) - float(totalcp)

            product = Product(name=name, stocks=stocks, cost_price=cp, selling_price=sp, totalcp=totalcp, totalsp=totalsp, exipry_date=edate, added_date=added_date, left_amount=left_amount, assumed_profit=assumed_profit )
            product.save()
        else:
            return render(request, 'shop/add-products.html')
        return render(request, 'shop/add-products.html')
    else:
        return redirect("shop:login_user")
# generate bill
def generate_bill(request):
    if request.user.is_superuser:
        carts = Cart.objects.all()
        # generate pdf of the bill
        total = Cart.objects.aggregate(Sum('amount'))['amount__sum']
        # create the folder
        directory = 'D:/Invoice/'+str(datetime.datetime.now().date())
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_dir = str(directory) + "/"+ str(random.randrange(5000, 20000)) + ".rtf"
        f = open(file_dir, "w")
        company = "\t\t\t\t\tBhandari Mart"
        address = "\t\t\t\t    Bhandaritole, Kathmandu"
        phone = "\t\t\t\t\t  9851183220"
        sample = "\t\t\t\t\t  Invoice"
        dt = "\t\t\t\t\t  " + str(datetime.datetime.now().date())

        table_header = "\n\n\t\t\t\t---------------------------------------\n\t\t\t\tS.N\tPr\t\tQty\tTotal\n\t\t\t\t---------------------------------------"
        final = company + "\n" + address + "\n" + phone + "\n" + sample + "\n" + dt + "\n" + table_header
        f.write(final)
        r = 1
        s = 1
        t = 2
        for c in carts:
            f.write("\n\t\t\t\t"+str(r) + "\t" + str(c.product.name)[:7] + "\t" + str(c.quantity) + "\t" + str(c.amount))
            r += 1
        # end contents #
        f.write("\n\n\n\t\t\t\t-------------------------\n\t\t\t\tTotal: Rs." + str(total) + "\n\t\t\t\t-------------------------")
        f.write("\n\n\n\t\t\t\tChecked By: Khimlal Bhandari")
        f.write("\n\t\t\t\tItems are non-refundable.")
        f.write("\n\t\t\t\tThank You For Visiting")
        f.close()

        os.startfile(file_dir ,"print")
        #print the bill

        # clear the cart
        carts = Cart.objects.all()
        for c in carts:
            c.delete()
        return redirect("shop:home")
    else:
        return redirect("shop:login_user")
def delete_item(request, id, pid):
    if request.user.is_superuser:
        carts = Cart.objects.get(product_id=id, id=pid)
        transactions = Transaction.objects.get(product_id=id, cart_id=pid)
        transactions.delete()

        product = Product.objects.get(id=carts.product_id)
        # get the purchased quantity
        pq = carts.quantity
        # add it to the stocks again
        product.stocks += pq
        product.save()
        carts.delete()
        return redirect("shop:home")
    else:
        return redirect("shop:login_user")
# update inventory
def update_stocks(request, slug):
    if request.user.is_superuser:
        details = Product.objects.get(slug=slug)
        text = "Update Old Stock"
        if request.method == 'POST':
            form = ProductForm(request.POST or None, instance=details)
            if form.is_valid():
                data = form.save(commit=False)
                data.totalcp = float(details.totalcp) + float(data.stocks) * float(data.cost_price)
                data.totalsp = int(details.totalsp) + int(data.stocks) * int(data.selling_price)
                data.left_amount = float(details.left_amount) + float(data.stocks) * float(data.cost_price)
                data.save()
                data.assumed_profit = float(data.totalsp - data.totalcp)
                data.save()
                # changing the totalcp/totalsp/left_amount/
                return redirect("shop:home")
        else:
            form = ProductForm(instance=details)
        return render(request, 'shop/updatestock.html', {'form': form, 'text': text})
    else:
        return redirect("shop:login_user")
def showupdate(request):
    if request.user.is_superuser:
        query = request.GET.get('id')
        if query:
            products = Product.objects.get(id=query)
            return render(request, 'shop/individual.html', {'products': products})
        products = Product.objects.all()
        page = request.GET.get('page', 1)

        paginator = Paginator(products, 25)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        context = {
            'products': products,
        }
        return render(request, 'shop/update-products-all.html', context)
    else:
        return redirect("shop:login_user")
# change name
def change_name(request, slug, id):
    if request.user.is_superuser:
        product = Product.objects.get(slug=slug, id=id)
        text = 'Change Name'
        if request.method == 'POST':
            form = UpdatenameForm(request.POST or None, instance=product)
            if form.is_valid():
                form.save()
                return redirect("shop:showupdate")
        else:
            form = UpdatenameForm(instance=product)
        return render(request, 'shop/updatestock.html', {'form':form, 'text':text})
    else:
        return redirect("shop:login_user")
# change price
def change_price(request, slug, id):
    if request.uesr.is_superuser:
        product = Product.objects.get(slug=slug, id=id)
        text = 'Change Price'
        if request.method == 'POST':
            form = PriceForm(request.POST or None, instance=product)
            if form.is_valid():
                form.save()
                return redirect("shop:showupdate")
        else:
            form = PriceForm(instance=product)
        return render(request, 'shop/updatestock.html', {'form':form, 'text':text})
    else:
        return redirect("shop:login_url")

# login user
def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('shop:home')
                else:
                    return render(request, 'shop/login.html', {'error_message': 'Your account has been disabled'})
            else:
                return render(request, 'shop/login.html', {'error_message': 'Invalid username or password'})
        return render(request, 'shop/login.html')
    else:
        return redirect("shop:login_user")

def stats(request):
    # all transactions from today
    today = datetime.datetime.now().date()
    transactions = Transaction.objects.filter(sold_on=today)

    # get the total sales
    total_sales = Transaction.objects.filter(sold_on=today).aggregate(Sum('total_amount'))['total_amount__sum']

    total_quantity = Transaction.objects.filter(sold_on=today).aggregate(Sum('quantity'))['quantity__sum']

    total_profit = Transaction.objects.filter(sold_on=today).aggregate(Sum('profit_or_loss'))['profit_or_loss__sum']


    context = {
        'transactions': transactions,
        'total_sales': total_sales,
        'total_quantity': total_quantity,
        'total_profit': total_profit,
        'today': today,
    }
    return render(request, 'shop/stats.html', context)