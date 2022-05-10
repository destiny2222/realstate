from os import name
from django.shortcuts import redirect, render
from django.contrib import messages
from real.models import *
from .forms import PropertyForm 
# Create your views here.

def homeview(request):
    property = Property.objects.all()[:6]
    find_location = Property.objects.all().filter()
    content = {'property':property, 'find_location':find_location}
    return render(request, 'index.html', content)


def AddProperity(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST or None, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index:home')
        else:
            return messages.info(request, 'helllllllllll')
    form = PropertyForm()    
    return render(request, 'property.html', {'form':form})    






  