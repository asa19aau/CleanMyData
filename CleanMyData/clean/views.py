from django.conf import settings
from django.shortcuts import render
from clean.models import Cleaner
from clean.forms.form import CleanerForm
from django.http import HttpResponseRedirect

def addCleaner(request):
    if request.method == 'POST':
        form = CleanerForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/success") 
    else:
        form = CleanerForm()
        

    return render(request, "entry.html", {
        "form": form
    })
    

def success(request):
    cleans = Cleaner.objects.order_by('id')
    return render(request, "success.html", {
        "cleans": cleans
    })