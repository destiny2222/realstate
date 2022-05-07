from django.shortcuts import redirect, render
from .forms import PropertyForm 
# Create your views here.

def homeview(request):

    return render(request, 'index.html')


def AddProperity(request):
    form = PropertyForm()
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index:home')
        else:
            form = PropertyForm()
    return render(request, 'property.html', {'form':form})    