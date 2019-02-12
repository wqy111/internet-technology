from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import PageForm

def index(request):

    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list, 'pages': page_list}
# Render the response and send it back!
    return render(request, 'rango/index.html', context_dict)
    #return HttpResponse("Rango says hey there partner!  <br/> <a href='/rango/about/'>About</a>")
def about(request):
    #return HttpResponse("Rango says here is the about page. <br/> <a href='/rango/'>Index</a>")
    # print(request.method)
    # # prints out the user name, if no one is logged in it prints `AnonymousUser`
    # print(request.user)
    return render(request, 'rango/about.html', {})

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
# We also add the category object from
# the database to the context dictionary.
# We'll use this in the template to verify that the category exists.
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango/category.html', context_dict)
# We get here if we didn't find the specified category.
# Don't do anything -
def add_category(request):
    form = CategoryForm()
# A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
    if form.is_valid():
        cat = form.save(commit=True)
        print(cat, cat.slug)
        return index(request)
    else:
        print(form.errors)
        return render(request, 'rango/add_category.html', {'form': form})
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}

    return render(request, 'rango/add_page.html', context_dict)
