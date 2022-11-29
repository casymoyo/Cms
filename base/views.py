from datetime import datetime, date, time, timedelta
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import render, redirect
from . models import User, Debtor, Work, Product
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . forms import debtorForm, workForm, productForm, paymentForm, createUserForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, login_required
# from django.contrib.auth.models import permissions


def loginpage(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username, password = password)
        if user is not None:    
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
    total_amount = Debtor()
    all_total_amounts = 0

    for debtor_amounts in total_amount.total:
        print(debtor_amounts)
        for amounts in debtor_amounts.values():
            all_total_amounts += amounts
    
    print(all_total_amounts)

    context = {
        'debtors': debtors.count(),
        'total': all_total_amounts
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
        # Q(product__icontains =  q)|
        Q(product__first_payment__icontains = q)|
        Q(product__second_payment__icontains = q)|
        Q(product__final_payment__icontains = q)|
        Q(work__employer__contains = q) 
    ) &  Debtor.objects.filter(user = request.user.id) & Debtor.objects.filter(status = '')
    
    overdue_thirty = Debtor()
    overdue_sixty = Debtor()
    overdue_ninety = Debtor()
    
    context = {
        'debtors': debtors,
        'overdue_thirty':overdue_thirty.due_in_thirty.count(),
        'overdue_sixty':overdue_thirty.due_in_sixty.count(),
        'overdue_ninety':overdue_thirty.due_in_ninety.count(),
        'cancelledCount':canclledCount,
    }
    return render(request, 'debtors/debtors.html', context)

@login_required(login_url = 'login')
def debtor(request, pk):
    deb = Debtor.objects.get(pk=pk)

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
            print(request.POST)
            debtor_obj = form.save(commit=False)
            debtor_obj.user = request.user
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
        return redirect('cancelledDebtorList')
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
            work_obj.id = deb.id
            work_obj.debtor_id = deb.id
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
    work = Work.objects.get(pk = pk)

    form = workForm(request.POST or None, instance = work)

    if form.is_valid():
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
    deb = Debtor.objects.get(pk = pk)
    form = productForm()
    if request.method == 'POST':
        form = productForm(request.POST)
        if form.is_valid():
            product_obj = form.save(commit = False)
            product_obj.id = deb.id
            product_obj.debtor_id = deb.id
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
    product = Product.objects.get(pk = pk)

    form = paymentForm(request.POST or None, instance = product)

    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, f'{product.debtor.name} payment details updated successfully')
        return redirect('debtors')
    context = {
        'form':form,
        'name': product.debtor.name
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
    for k in users:
        print(k['position'])
    return render(request, 'user/userManagement.html', {'users': users})

@login_required(login_url = 'login')
def createUser(request):
    # permissions = Permissions.objects.all()
    # print(permissions)
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        print(request.POST)
        if form.is_valid:
            user_obj = form.save(commit = False)
            # if user_obj.position == 'sales':
            #     g = Group.objects.get(name='Sales') 
            #     g.user_set.add(user_obj)
            form.save()

        g = Group.objects.get(name='sales')
        users = User.objects.all()
        for u in users:
            print(u)
            # g.user_set.add(u)
    return render(request,'user/createUser.html', {'form':form} )  