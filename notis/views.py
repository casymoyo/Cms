from django.shortcuts import render
from base.models import Debtor
from . models import Notifications, User

def activity(request, pk):
    try:
        debtor = Debtor.objects.get(pk=pk)
    except Debtor.DoesNotExist:
        pass
    notis =  Notifications.objects.filter(partial_id = debtor.phonenumber)
    print(notis)
    context = {
        "activities":notis
    }
    return render(request, 'debtors/activities/activities.html', context)

def userActivity(request, pk):
    try:
        notis =  Notifications.objects.filter(user = pk)
    except:
        print('no data')
    return render(request, 'user/userActivity.html', {'activities':notis})