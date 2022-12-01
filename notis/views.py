from django.shortcuts import render
from base.models import Debtor
from . models import Notifications

def activity(request):
    # debtor = Debtor.objects.get(pk=pk)
    notis =  Notifications.objects.filter()
    print(notis)
    context = {
        "activities":notis
    }
    return render(request, 'debtors/activities/activities.html', context)
