from django.shortcuts import render

def getMyAccountPage(request):
    return render(request, 'myaccount.html')
