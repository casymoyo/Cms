from datetime import datetime, date, time, timedelta
from django.http import HttpResponse
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import render, redirect
from . models import User, Debtor, Work, Product
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . forms import debtorForm, workForm, productForm, paymentForm, UpdatePaymentForm, updateProductForm, createUserForm, updateUserForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required, login_required
from json import dumps
from notis.models import Notifications
from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth.models import permissions


def loginpage(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username = username, password = password)
        if user is not None:    
            request.session['username'] = username
            login(request, user)
            
            if request.user.position == 'admin':
                return redirect('adminDashboard')
            else:
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
    if request.user.position != 'admin':
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        notis = Notifications.objects.filter(Q(created__icontains = q))
        debtors = Debtor.objects.filter(user = request.user.id)
        try:
            fully_paid = Debtor.objects.filter(is_fully_paid = 'yes') & Debtor.objects.filter(user  = request.user.id)
        except:
            pass
        total_sp = debtors.aggregate(Sum('product__product_amount'))
        total_dp = debtors.aggregate(Sum('product__deposit'))
        debtor_thirty_amounts = debtors.aggregate(Sum('product__first_payment'))
        debtor_sixty_amounts = debtors.aggregate(Sum('product__second_payment')) 
        debtor_final_amounts = debtors.aggregate(Sum('product__final_payment'))

        overdues_count = Debtor()
        overdues = Debtor()

        totals = 0
        
        try:
            totals = total_dp['product__deposit__sum'] + debtor_thirty_amounts['product__first_payment__sum'] + debtor_sixty_amounts['product__second_payment__sum'] + debtor_final_amounts['product__final_payment__sum']
        except:
            pass
        print(debtor_thirty_amounts)
        context = {
            'debtors': debtors.count(),
            'total':totals ,
            'activities': notis,
            'total_sp': total_sp['product__product_amount__sum'],
            'fully_paid': fully_paid.count(),
            'overdues_count': overdues_count.due_in_thirty.count() + overdues_count.due_in_sixty.count() + overdues_count.due_in_ninety.count() 
        }
        return render(request, 'dashboard.html', context)
    else:
        return redirect('adminDashboard')

@login_required(login_url = 'login')
def adminDashboard(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    notis = Notifications.objects.filter(Q(created__icontains = q))
    canclledCount = Debtor.objects.filter(status = 'cancelled').count()
    debtors = Debtor.objects.all()
    fully_paid = Debtor.objects.filter(is_fully_paid = 'yes').count()
    total_sp = Debtor.objects.aggregate(Sum('product__product_amount'))
    total_dp = Debtor.objects.aggregate(Sum('product__deposit'))
    overdues_count = Debtor()
    overdues = Debtor()
    total_amount = Debtor()
    all_total_amounts = 0
    totals = 0
    
    for debtor_amounts in total_amount.total:
        for amounts in debtor_amounts.values():
            try:
                all_total_amounts = amounts + all_total_amounts
            except:
                pass
    
    try:
        totals = all_total_amounts + total_dp['product__deposit__sum'] 
    except:
        pass
    context = {
        'total':totals ,
        'activities': notis,
        'debtors': debtors.count(),
        'cancelledCount':canclledCount,
        'total_sp': total_sp['product__product_amount__sum'],
        'fully_paid': fully_paid,
        'overdues_count': overdues_count.due_in_thirty.count() + overdues_count.due_in_sixty.count() + overdues_count.due_in_ninety.count() 
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url = 'login')
def debtors(request):
        if request.user.position != 'admin':
            q = request.GET.get('q') if request.GET.get('q') != None else ''
            debtors = Debtor.objects.filter(
                Q(name__icontains =  q)|
                Q(created__icontains =  q)|
                Q(product__deposit__icontains =  q)|
                Q(product__first_payment__icontains = q)|
                Q(product__second_payment__icontains = q)|
                Q(product__final_payment__icontains = q)|
                Q(work__employer__contains = q) 
            ) &  Debtor.objects.filter(user = request.user.id) & Debtor.objects.filter(status = '') & Debtor.objects.filter(is_fully_paid = 'no')
            overdues = Debtor()
            
            context = {
                'debtors': debtors,
                'overdue_thirty':overdues.due_in_thirty.count(),
                'overdue_sixty':overdues.due_in_sixty.count(),
                'overdue_ninety':overdues.due_in_ninety.count(),
            }
            return render(request, 'debtors/debtors.html', context)
        else:
            q = request.GET.get('q') if request.GET.get('q') != None else ''
            debtors = Debtor.objects.filter(
                Q(name__icontains =  q)|
                Q(created__icontains =  q)|
                Q(product__deposit__icontains =  q)|
                Q(product__first_payment__icontains = q)|
                Q(product__second_payment__icontains = q)|
                Q(product__final_payment__icontains = q)|
                Q(work__employer__contains = q) 
            ) &  Debtor.objects.all() & Debtor.objects.filter(status = '') & Debtor.objects.filter(is_fully_paid = 'no')
            overdues = Debtor()
            
            context = {
                'debtors': debtors,
                'overdue_thirty':overdues.due_in_thirty.count(),
                'overdue_sixty':overdues.due_in_sixty.count(),
                'overdue_ninety':overdues.due_in_ninety.count(),
            }
            print((context))
            return render(request, 'debtors/debtors.html', context)


@login_required(login_url = 'login')
def debtor(request, pk):
    try:
        deb = Debtor.objects.get(pk=pk)
    except:
        return render(request, '404.html')
    context = {
        'debtor': deb,
    }
    return render(request, 'debtors/debtor.html', context)

@permission_required('base.add_debtor')
@login_required(login_url = 'login')
def createDebtor(request):
    debtors = Debtor.objects.all()
    form = debtorForm()
    if request.method == 'POST':
        form = debtorForm(request.POST)
        # custom validation 
        id_number = request.POST['id_number']
        phonenumber = request.POST['phonenumber']
        if len(id_number) < 10 or len(phonenumber) < 10:
            messages.add_message(request, messages.WARNING, f'Check if Id number and phonenumber are correct')
            return render(request, 'debtors/createDebtor.html', {'form': form})
        if form.is_valid():
            debtor_obj = form.save(commit=False)
            debtor_obj.user = request.user
            # creating notfication
            notis, created = Notifications.objects.get_or_create(
                user = request.user,
                title = f'{debtor_obj.name}',
                content = f'Account Created',
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
    try:
        debtor = Debtor.objects.get(pk=pk)
    except:
        return render(request, '404.html')

    if debtor.status != 'cancelled':
        debtor.status = 'cancelled'
        # creating a nofication
        notis, created = Notifications.objects.get_or_create(
                user = request.user,
                title = f'{debtor.name}',
                content = f'Account Cancelled',
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
    try:
        debtor = Debtor.objects.get(pk=pk)
    except:
        return render(request, '404.html')

    if debtor.status == 'cancelled':
        debtor.status = ''
        debtor.save()
        messages.add_message(request, messages.SUCCESS, f'{debtor.name} cancellation successfully reverted')
        return redirect('debtors')
    else:
        messages.add_message(request, messages.WARNING, f'{debtor.name} cancellation not reverted')
        return redirect('cancelledDebtorList')

@login_required(login_url = 'login')
def deleteDebtor(request, pk):
    try:
        debtor = Debtor.objects.get(pk = pk)
        debtor.delete()
    except:
        return render(request, '404.html')
    return redirect('cancelledDebtorList')

@login_required(login_url = 'login')
def fullyPaidDebtors(request):
    debtors = Debtor.objects.filter(is_fully_paid = 'yes')
    return render(request, 'debtors/fullyPaidDebtors.html', {'debtors':debtors})

# debtor work details
@login_required(login_url = 'login')
def createWork(request, pk):
    try:
        deb = Debtor.objects.get(pk = pk)
    except:
        return render(request, '404.html')

    form = workForm()

    if request.method == 'POST':
        form = workForm(request.POST)
        if form.is_valid():
            work_obj = form.save(commit = False)
            work_obj.work_id = deb.id
            work_obj.debtor_id = deb.id
            # creating a nofication
            notis, created = Notifications.objects.get_or_create(
                user = request.user,
                title = f'{work_obj.debtor.name}',
                content = f'Created Work Details',
                partial_id = work_obj.debtor.phonenumber
            )
            #saving notificatioin object
            work_obj.save()
            return redirect('debtor', pk = pk)
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
    try:
        work = Work.objects.get(pk = pk)
    except:
        return render(request, '404.html')

    form = workForm(request.POST or None, instance = work)

    if form.is_valid():
        # creating a nofication
        notis, created = Notifications.objects.get_or_create(
            user = request.user,
            title = f'{work.debtor.name}',
            content = f'Updated work details',
            partial_id = work.debtor.phonenumber
        )
        #saving notificatioin object
        notis.save()
        #saving form
        form.save()
        messages.add_message(request, messages.SUCCESS, f'{work.debtor.name} work details updated successfully')
        return redirect('debtor', pk = pk)
    context = {
        'form':form,
        'name': work.debtor.name
    }
    return render(request, 'debtors/createWork.html', context)

@login_required(login_url = 'login')
def createProduct(request, pk):
    try:
        deb = Debtor.objects.get(pk = pk)
    except:
        return render(request, '404.html')

    form = productForm()
    if request.method == 'POST':
        form = productForm(request.POST)
        # validation
        product_amount = request.POST['product_amount']
        deposit =  request.POST['deposit']
        if int(product_amount) < 0 or int(deposit) < 0:
            messages.add_message(request, messages.Warning, f'The deposit amount or product amount should not be less than 0')
            return render(request, 'debtors/createProduct.html', {'form': form})
        else:
            if form.is_valid():
                product_obj = form.save(commit = False)
                product_obj.product_id = deb.id
                product_obj.debtor_id = deb.id
                product_obj.total = request.POST['deposit']
                # creating notification
                notis, created = Notifications.objects.get_or_create(
                    user = request.user,
                    title = f'{deb.name}',
                    content = f'Created Product Details',
                    partial_id = deb.phonenumber #for notification look up
                )
                #saving notificatioin object
                product_obj.save()
                messages.add_message(request, messages.SUCCESS, 'Product details successfully added')
                return redirect('debtor', pk = pk)
            else:
                messages.add_message(request, messages.WARNING, '* fill in all the required details')
                return redirect('createProduct', pk)
    context = {
        'form':form
    }
    return render(request, 'debtors/createProduct.html', context)

@login_required(login_url = 'login')
def updateProduct(request, pk):
    try:
        product = Product.objects.get(pk = pk)
    except:
        return render(request, '404.html')

    form = updateProductForm(request.POST or None, instance = product)

    if form.is_valid():
        product_obj = form.save(commit = False)
        
        if product_obj.product_amount < 0 or product_obj.deposit < 0:
            messages.add_message(request, messages.WARNING, f'The deposit amount or product amount should not be less than 0')
            return render(request, 'debtors/createProduct.html', {'form':form})
        # creating notification
        notis, created = Notifications.objects.get_or_create(
            user = request.user,
            title = f'{product.debtor.name}',
            content = f'Updated Product Details',
            partial_id = product.debtor.phonenumber
            )
        #saving notificatioin object
        product_obj.save()
        messages.add_message(request, messages.SUCCESS, f'{product.debtor.name} product details updated successfully')
        return redirect('debtor', pk = pk)
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
    try:
        product = Product.objects.get(pk = pk)
        debtor = Debtor.objects.get(pk = pk)
    except :
        return render(request, '404.html')

    amount['product_amount'] = str(product.product_amount)
    dataJSON = dumps(amount)

    form = UpdatePaymentForm(request.POST or None, instance = product)

    if form.is_valid():
        payment_obj = form.save(commit = False)
        payment_obj.total = product.deposit + product.first_payment + product.second_payment + product.final_payment
        if product.deposit + payment_obj.first_payment == product.product_amount:
            debtor.is_fully_paid = 'yes'
            debtor.save()
        elif product.deposit + product.first_payment + payment_obj.second_payment == product.product_amount:
            debtor.is_fully_paid = 'yes'
            debtor.save()
        elif product.deposit + product.first_payment + product.second_payment + payment_obj.final_payment == product.product_amount:
            debtor.is_fully_paid = 'yes'
            debtor.save()
        # creating notification
        notis, created = Notifications.objects.get_or_create(
            user = request.user,
            title = f'{product.debtor.name}',
            content = f'Updated Payment',
            partial_id = product.debtor.phonenumber
            )
        #saving notificatioin object
        payment_obj.save()
        return redirect('debtor', pk = pk)

    context = {
        'form':form,
        'name': product.debtor.name,
        'data': dataJSON,
        'product': product,

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
    return render(request, 'user/userManagement.html', {'users': users})

@login_required(login_url = 'login')
def createUser(request):
    # permissions = Permissions.objects.all()
    # print(permissions)
    form = createUserForm()
    if request.method == 'POST':
        form = createUserForm(request.POST)
        
        if form.is_valid:
            user = form.save(commit = False)
            user.is_staff = True
            user.save()
            return redirect('userManagement')
    return render(request,'user/createUser.html', {'form':form} )  

@login_required(login_url = 'login')
def updateUser(request, pk):
    user = User.objects.get(pk = pk)
    form = updateUserForm()
    if request.method == 'POST':
        form = updateUserForm(request.POST, request.FILES or None, instance=user)
        
        if form.is_valid:
            form.save()
    return render(request, 'user/editProfile.html', {'user':user, 'form':form})

@login_required(login_url = 'login')
def userDebtors(request, pk):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    debtors = Debtor.objects.filter(
        Q(user = pk) |
        Q(name__icontains =  q)|
        Q(created__icontains =  q)|
        Q(product__deposit__icontains =  q)|
        Q(product__first_payment__icontains = q)|
        Q(product__second_payment__icontains = q)|
        Q(product__final_payment__icontains = q)|
        Q(work__employer__contains = q)
    ) & Debtor.objects.filter(user = pk)
    return render(request, 'user/userDebtors.html', {'debtors':debtors})

@login_required(login_url = 'login')
def userSettings(request, pk):
    try:
        user = User.objects.get(pk = pk)
    except:
        return render(request, '404.html')

    return render(request, 'user/settings.html', {'user':user})

def userPermissions(request, pk):
    try:
        user = User.objects.get(pk = pk)
    except:
        return render(request, '404.html')

    if user.position == 'sales':
        g = Group.objects.get(name='Sales')
        g.user_set.add(user)
        messages.add_message(request, messages.SUCCESS, f'{user.username} {g.name} permissions successfully added')

    elif user.position == 'admin':
        g = Group.objects.get(name='Admin')
        g.user_set.add(user)
        messages.add_message(request, messages.SUCCESS, f'{user.username} {g.name} permissions successfully added')
    
    elif user.position == 'accountant':
        g = Group.objects.get(name='Accounts')
        g.user_set.add(user)
        messages.add_message(request, messages.SUCCESS, f'{user.username} {g.name} permissions successfully added')
    
    elif user.position == 'team leader':
        g = Group.objects.get(name='Team Leader')
        g.user_set.add(user)
        messages.add_message(request, messages.SUCCESS, f'{user.username} {g.name} permissions successfully added')

    return redirect('userManagement')

@login_required(login_url = 'login')
def changeUserPassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('changeUserPassword')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

def generatePdf(request, pk):
    pass