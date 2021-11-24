from django.shortcuts import render
from clean.models import File, Preferences
from clean.forms.form import CleanerForm
from django.http import HttpResponseRedirect

def addCleaner_view(request):
    if request.method == 'POST':
        form = CleanerForm(request.POST, request.FILES)
        
        if form.is_valid():
            file = form.save()
            
            file_preferences = Preferences.objects.create(file=file)
            file_preferences.save()
            
            return HttpResponseRedirect("/preferences/" + str(file_preferences.id)) 
    else:
        form = CleanerForm()
        

    return render(request, "entry.html", {
        "form": form
    })
    

def success_view(request):
    files = File.objects.order_by('id')
    return render(request, "success.html", {
        "files": files
    })
    

def preferences_view(request, pk):
    print(pk)
    return render(request, "preferences.html", {
        "preferences": pk
    })

def help_view(request):
    return render(request, "help.html")