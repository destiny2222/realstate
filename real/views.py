from django.shortcuts import redirect, render,get_object_or_404
from django.contrib import messages
from django.http import   Http404
from real.models import *
from .forms import PropertyForm
from .choices import bedroom_choices, properity_type_choices ,bath_rooms_choices
from django.core.paginator import  Paginator, PageNotAnInteger, EmptyPage
# Create your views here.

def homeview(request):
    property = Listing.objects.order_by('-list_date').all()[:6]
    find_location = Listing.objects.all().filter()
    content = {
        'property':property, 
        'find_location':find_location,
        'properity_type_choices': properity_type_choices,
        'bedroom_choices': bedroom_choices,
        'bath_rooms_choices': bath_rooms_choices,
        'values': request.POST
        }
    return render(request, 'index.html', content)


def AddProperity(request):
    if request.method == 'POST':
        # print(request.POST)
        form = PropertyForm(request.POST , files=request.FILES)
        if form.is_valid():
            form.save()
            messages.info(request, 'Property Added Successful')
            return redirect('index:home')
        else:
            messages.error(request, form.errors)
    form = PropertyForm()    
    return render(request, 'property.html', {'form':form})    


def ProperityView(request):
    pro_view = Listing.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(pro_view, 3)
    try:
        pro_view = paginator.page(page)
    except PageNotAnInteger:
        # if is not an integer, deliver the first page
        pro_view = paginator.page(1)
    except EmptyPage:
        # if the page is out of range deliver the last page
        pro_view = paginator.page(paginator.num_pages) 
    content = {'pro_view':pro_view, 'page':page,}
    return render(request, 'property-view.html', content)

def DetailsViews(request, slug):
    single = Listing.objects.filter(slug=slug)
    if single.exists():
        single = Listing.objects.get(slug=slug)
    else:
        return redirect("index:404") 
    content = {'single':single}    
    return render(request, 'single-property.html', content)

def Error404(request):

    return render(request, '404.html')    


def AboutView(request):
    return render(request, 'about-us.html')


def search(request):
    queryset_list = Listing.objects.order_by('-list_date')
    # KEYWORDS
    
    if 'address' in request.POST:
        address = request.POST['address']
        if address:
            queryset_list = queryset_list.filter(address__icontains=address)

    # CITY
    if 'city' in request.POST:
        city = request.POST['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # STATE
    if 'state' in request.POST:
        state = request.POST['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # BEDROOMS
    if 'bedrooms' in request.POST:
        bedrooms = request.POST['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # BATHROOM
    if 'property_type' in request.POST:
        property_type = request.POST['property_type']
        if property_type:
            queryset_list = queryset_list.filter(property_type__lte=property_type)



    # PRICE
    if 'price' in request.POST:
        price = request.POST['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'listings': queryset_list,
    }

    return render(request, 'sarech.html', context)




  
  