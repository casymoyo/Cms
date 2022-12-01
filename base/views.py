from datetime import datetime, date, time, timedelta
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import render, redirect
from . models import User, Debtor, Work, Product
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . forms import debtorForm, workForm, productForm, paymentForm, UpdatePaymentForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, login_required
from json import dumps
from notis.models import Notifications
# from django.contrib.auth.models import permissions


def loginpage(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        if user is not None:    
            request.session['username'] = username
            login(request, user)
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.WARNING, 'login failed')
            return redirect('login')
    return render(request, 'user/login.html', {})

def logoutpage(request):
    logout(request)
    return redirect('/')

@login_required(login_url = 'login')
def dashboard(request):
    debtors = Debtor.objects.all()
    notis = Notifications.objects.all()
    overdues = Debtor()
    total_amount = Debtor()
    all_total_amounts = 0

    
    for debtor_amounts in total_amount.total:
        for amounts in debtor_amounts.values():
            try:
                all_total_amounts = amounts + all_total_amounts
            except:
                pass
    context = {
        'debtors': debtors.count(),
        'total': all_total_amounts,
        'activities': notis
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url = 'login')
def debtors(request):
    canclledCount = Debtor.objects.filter(status = 'cancelled').count()
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    debtors = Debtor.objects.filter(
        Q(name__icontains =  q)|
        Q(created__icontains =  q)|
        Q(product__deposit__icontains =  q)|
        Q(product__first_payment__icontains = q)|
        Q(product__second_payment__icontains = q)|
        Q(product__final_payment__icontains = q)|
        Q(work__employer__contains = q) 
    ) &  Debtor.objects.filter(user = request.user.id) & Debtor.objects.filter(status = '') 
    # p = Product.objects.get(pk = 2)
    # print(p)
    overdues = Debtor()
    
    context = {
        'debtors': debtors,
        'overdue_thirty':overdues.due_in_thirty.count(),
        'overdue_sixty':overdues.due_in_sixty.count(),
        'overdue_ninety':overdues.due_in_ninety.count(),
        'cancelledCount':canclledCount,
    }
    print((context))
    return render(request, 'debtors/debtors.html', context)

@login_required(login_url = 'login')
def debtor(request, pk):
    try:
        deb = Debtor.objects.get(pk=pk)
    except Debtor.DoesNotExist:
        return HttpResponse(status=404)
    context = {
        'debtor': deb
    }
    return render(request, 'debtors/debtor.html', context)

@permission_required('base.add_debtor')
@login_required(login_url = 'login')
def createDebtor(request):
    debtors = Debtor.objects.all()
    form = debtorForm()
    if request.method == 'POST':
        form = debtorForm(request.POST)
        if form.is_valid():
            debtor_obj = form.save(commit=False)
            debtor_obj.user = request.user
            # creating notfication
            notis, created = Notifications.objects.get_or_create(
                user = request.user,
                title = f'{debtor_obj.name}',
                content = f'{request.user} Created {debtor_obj.name}',
                partial_id = debtor_obj.phonenumber
            )
            #saving notificatioin object
            notis.save()
            #saving debtor object
            debtor_obj.save()
            return redirect('debtors')
            messages.add_message(request, messages.SUCCESS, 'Debtor successfully added')
        else:
            messages.add_message(request, messages.WARNING, '* fill in all the required details')
            return redirect('createDebtor')  
    context = {
        'form':form
    }
    return render(request, 'debtors/createDebtor.html', context)

@login_required(login_url = 'login')
def cancelledDebtorList(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    cancelledDebtors = Debtor.objects.filter(
        Q(name__icontains =  q)|
        Q(created__icontains =  q)
    ) & Debtor.objects.filter(status = 'cancelled')
    return render(request, 'debtors/cancel/cancelledDebtors.html', {'cancelledDebtors':cancelledDebtors})

@login_required(login_url = 'login')
def cancelDebtor(request, pk):
    debtor = Debtor.objects.get(pk=pk)
    if debtor.status != 'cancelled':
        debtor.status = 'cancelled'
        # creating a nofication
        notis, created = Notifications.objects.get_or_create(
                user = request.user,
                title = f'{debtor.name}',
                content = f'{request.user} Cancelled {debtor.name}',
            )
        #saving notificatioin object
        notis.save()
        debtor.save()
        messages.add_message(request, messages.SUCCESS, f'{debtor.name} was successfully cancelled')
        return redirect('debtors')
    else:
        messages.add_message(request, messages.WARNING, f'{debtor.name} was already cancelled')
        return redirect('debtors')

@login_required(login_url = 'login')
def revertCancellation(request, pk):
    debtor = Debtor.objects.get(pk=pk)
    if debtor.status == 'cancelled':
        debtor.status = ''
        debtor.save()
        messages.add_message(request, messages.SUCCESS, f'{debtor.name} cancellation successfully reverted')
        return redirect('debtors')
    else:
        messages.add_message(request, messages.WARNING, f'{debtor.name} cancellation not reverted')
        return redirect('cancelledDebtorList')

# debtor work details
@login_required(login_url = 'login')
def createWork(request, pk):
    deb = Debtor.objects.get(pk = pk)
    form = workForm()

    if request.method == 'POST':
        form = workForm(request.POST)
        if form.is_valid():
            work_obj = form.save(commit = False)
            work_obj.work_id = deb.id
            print(work_obj.work_id)
            work_obj.debtor_id = deb.id
            # creating a nofication
            notis, created = Notifications.objects.get_or_create(
                user = request.user,
                title = f'{work_obj.debtor.name}',
                content = f'{request.user} Created Work Details for {work_obj.debtor.name}',
            )
            #saving notificatioin object
            work_obj.save()
            return redirect('debtors')
            messages.add_message(request, messages.SUCCESS, 'Work details successfully added')
        else:
            messages.add_message(request, messages.WARNING, '* fill in all the required details')
            return redirect('createDebtor')
    context = {
        'form':form
    }
    return render(request, 'debtors/createWork.html', context)

@login_required(login_url = 'login')
def updateWork(request, pk):
    work = Work.objects.get(id = pk)

    form = workForm(request.POST or None, instance = work)

    if form.is_valid():
        # creating a nofication
        notis, created = Notifications.objects.get_or_create(
            user = request.user,
            title = f'{work.debtor.name}',
            content = f'{request.user} Updated work details {work.debtor.name}',
        )
        #saving notificatioin object
        notis.save()
        form.save()
        messages.add_message(request, messages.SUCCESS, f'{work.debtor.name} work details updated successfully')
        return redirect('debtors')
    context = {
        'form':form,
        'name': work.debtor.name
    }
    return render(request, 'debtors/createWork.html', context)

@login_required(login_url = 'login')
def createProduct(request, pk):
    try:
        deb = Debtor.objects.get(pk = pk)
    except deb.DoesNotExist:
        return HttpResponse(status=404)

    form = productForm()
    if request.method == 'POST':
        form = productForm(request.POST)
        if form.is_valid():
            product_obj = form.save(commit = False)
            product_obj.product_id = deb.id
            product_obj.debtor_id = deb.id
            product_obj.total = request.POST['deposit']
            # creating notification
            notis, created = Notifications.objects.get_or_create(
            user = request.user,
            title = f'{deb.name}',
            content = f'{request.user} Created Product Details For {deb.name}',
            )
            #saving notificatioin object
            product_obj.save()
            return redirect('debtors')
            messages.add_message(request, messages.SUCCESS, 'Product details successfully added')
        else:
            messages.add_message(request, messages.WARNING, '* fill in all the required details')
            return redirect('createProduct')
    context = {
        'form':form
    }
    return render(request, 'debtors/createProduct.html', context)

@login_required(login_url = 'login')
def updateProduct(request, pk):
    product = Product.objects.get(pk = pk)

    form = productForm(request.POST or None, instance = product)

    if form.is_valid():
        # creating notification
        notis, created = Notifications.objects.get_or_create(
            user = request.user,
            title = f'{product.debtor.name}',
            content = f'{request.user} Updated Product Details For {product.Debtor.name}',
            )
        #saving notificatioin object
        form.save()
        messages.add_message(request, messages.SUCCESS, f'{product.debtor.name} product details updated successfully')
        return redirect('debtors')
    context = {
        'form':form,
        'name': product.debtor.name
    }
    return render(request, 'debtors/createProduct.html', context)

@login_required(login_url = 'login')
def payment(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    debtors = Debtor.objects.filter(
        Q(name__icontains =  q)|
        Q(surname__icontains = q)
    )&  Debtor.objects.filter(user = request.user.id)
    
    context = {
        'debtors':debtors
    }
    return render(request, 'debtors/payment.html', context)

@login_required(login_url = 'login')
def updatePayment(request, pk):
    amount ={}
    product = Product.objects.get(pk = pk)
    
    amount['product_amount'] = str(product.product_amount)
    dataJSON = dumps(amount)

    form = UpdatePaymentForm(request.POST or None, instance = product)

    if form.is_valid():
        payment_obj = form.save(commit = False)
        payment_obj.total = product.deposit + product.first_payment + product.second_payment + product.final_payment
        if product.deposit + payment_obj.first_payment == product.product_amount:
            payment_obj.is_fully_paid = 'yes'
        elif product.deposit + product.first_payment + payment_obj.second_payment == product.product_amount:
            payment_obj.is_fully_paid = 'yes'
        elif product.deposit + product.first_payment + product.second_payment + payment_obj.final_payment == product.product_amount:
            payment_obj.is_fully_paid = 'yes'
        # creating notification
        notis, created = Notifications.objects.get_or_create(
            user = request.user,
            title = f'{product.debtor.name}',
            content = f'{request.user} Updated Payments For {product.debtor.name}',
            )
        #saving notificatioin object
        payment_obj.save()
        messages.add_message(request, messages.SUCCESS, f'{product.debtor.name} payment details updated successfully')
        return redirect('debtors')

    context = {
        'form':form,
        'name': product.debtor.name,
        'data': dataJSON
    }
    return render(request, 'debtors/createPayment.html', context)

# overdues

@login_required(login_url = 'login')
def overdues(request):
    overdues = Debtor()
    print(overdues.due_in_sixty)

    
    context = {
        'overdue_thirty':overdues.due_in_thirty,
        'overdue_sixty':overdues.due_in_sixty,
        'overdue_ninety':overdues.due_in_ninety,
    }
    
    return render(request, 'debtors/overdues/overdues.html', context)

@login_required(login_url = 'login')
def firstOverdues(request):
    overdues = Debtor()

    context = {
        'overdue_thirty':overdues.due_in_thirty,
    }
    
    return render(request, 'debtors/overdues/firstOverdues.html', context)

@login_required(login_url = 'login')
def secondOverdues(request):
    overdues = Debtor()

    context = {
        'overdue_sixty':overdues.due_in_sixty,
    }
    
    return render(request, 'debtors/overdues/secondOverdues.html', context)

@login_required(login_url = 'login')
def finalOverdues(request):
    overdues = Debtor()

    context = {
        'overdue_ninety':overdues.due_in_ninety,
    }
    
    return render(request, 'debtors/overdues/finalOverdues.html', context)

# Users
@login_required(login_url = 'login')
def userManagement(request):
    users = User.objects.all()
    print(users)
    return render(resquest, 'user/userManagement.html', {'users': users})

@login_required(login_url = 'login')
def createUser(request):
    # permissions = Permissions.objects.all()
    # print(permissions)
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        print(request.POST)
        if form.is_valid:
            # user_obj = form.save(commit = False)
            # if user_obj.position == 'sales':
            #     g = Group.objects.get(name='Sales') 
            #     g.user_set.add(user_obj)
            form.save()

        # g = Group.objects.get(name='sales')
        # users = User.objects.all()
        # for u in users:
        #     print(u)
            # g.user_set.add(u)
    return render(request,'user/createUser.html', {'form':form} )  

# activities

