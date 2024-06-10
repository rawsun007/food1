# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, redirect, render

from .models import *



@login_required(login_url="/login_page/")
def add(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        about = data.get('about')
        img = request.FILES.get('img')

        if data and name and img:
            fastfood.objects.create(name=name, about=about, img=img)
            return redirect("/home/")

        else:
            messages.error(request, "enter data")
            return redirect("/add/")


    
    queryset = fastfood.objects.all()  
    context = {'recipes': queryset}
    return render(request, "add.html", context)

@login_required(login_url="/login_page/")
def home(request):
    queryset = fastfood.objects.all()

    if 'Search' in request.GET:
        recipe_name = request.GET.get('Search')
        queryset = queryset.filter(name__icontains=recipe_name)
        if not queryset:
            messages.error(request, "Recipe not found")
    
    paginator = Paginator(queryset, 3)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'queryset': page_obj, 'recipe': queryset})
    


@login_required(login_url="/login_page/")
def delete_re(request,id):
     queryset=fastfood.objects.get(id = id)
     queryset.delete()

     return redirect("/home/")

@login_required(login_url="/login_page/")
def update_re(request,id):
     queryset=fastfood.objects.get(id = id)

     if request.method == 'POST':
        data = request.POST
        print(data)
        name = data.get('name')
        print(name)
        about = data.get('about')
        print(about)
        
        img = request.FILES.get('img')
        print(img)

        queryset.name = name
        queryset.about = about
        if img:
            queryset.img = img
        queryset.save()
        
        return redirect("/home/")
        
     context = {'recipe': queryset}


     return render(request, "update_re.html",context)



def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist")
            return redirect("/login_page/")

        user = authenticate(username=username, password=password)


        if user is not None:
            login(request, user)

            return redirect("/home/")  
        else:
            messages.error(request, "Invalid password")
   

            return redirect("/login_page/")

    return render(request, "login_page.html")


def logout_page(request):

    logout(request)
    return redirect('/login_page/')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        

        if User.objects.filter(username=username).exists():
            messages.error(request, " username alredy taken")
            return redirect("/signup/")



        user = User.objects.create(
        first_name = first_name,
        last_name = last_name,
        username=username
         )
        user.set_password(password)
        user.save()



        messages.info(request, "acoount created !")

        return redirect("/login_page/")  
    
    return render(request, "signup.html")


from django.core.mail import send_mail


def test_email(request):
    send_mail(
        'bhai ',
        'chage password ',
        'test007.for.web@gmail.com',
        ['roshanramani.dev@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("Email sent")