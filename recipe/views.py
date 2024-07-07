# Create your views here.
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import HttpResponse, redirect, render

from .models import fastfood


@login_required(login_url="/recipe/login_page/")
def add(request):
    if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        about = data.get('about')
        img = request.FILES.get('img')

        if data and name and img:
            fastfood.objects.create(name=name, about=about, img=img)
            return redirect("/recipe/home/")
        else:
            messages.error(request, "Please enter all required data")
            return redirect("/recipe/add/")
    
    queryset = fastfood.objects.all()  
    context = {'recipes': queryset}
    return render(request, "recipe/add.html", context)


@login_required(login_url="/recipe/login_page/")
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

    return render(request, 'recipe/home.html', {'queryset': page_obj, 'recipe': queryset})


@login_required(login_url="/recipe/login_page/")
def delete_re(request, id):
    #  queryset = fastfood.objects.get(id=id)
    #  queryset.delete()
     queryset = SavedRecipe.objects.get(id=id)
     queryset.delete()
     return redirect("/recipe/user_pro/")


@login_required(login_url="/recipe/login_page/")
def update_re(request, id):
     queryset = fastfood.objects.get(id=id)

     if request.method == 'POST':
        data = request.POST
        name = data.get('name')
        about = data.get('about')
        img = request.FILES.get('img')

        queryset.name = name
        queryset.about = about
        if img:
            queryset.img = img
        queryset.save()
        
        return redirect("/recipe/home/")
        
     context = {'recipe': queryset}
     return render(request, "recipe/update_re.html", context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist")
            return redirect("/recipe/login_page/")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/recipe/home/")
        else:
            messages.error(request, "Invalid password")
            return redirect("/recipe/login_page/")

    return render(request, "recipe/login_page.html")


def logout_page(request):
    logout(request)
    return redirect('/recipe/login_page/')


def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect("/recipe/signup/")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username
        )
        user.set_password(password)
        user.save()

        messages.info(request, "Account created!")
        return redirect("/recipe/login_page/")
    
    return render(request, "recipe/signup.html")



from django.shortcuts import render

from .utils import fetch_recipes


def recipe_list(request):
    recipe_name = request.GET.get('Search', '')
    next_url = request.GET.get('next_url', None)

    recipes, next_page_url = fetch_recipes(recipe_name, next_url)

    # Debug logging
    # print("Recipes:", recipes)
    print("Next Page URL:", next_page_url)

    return render(request, 'recipe/recipe_list.html', {
        'recipes': recipes,
        'next_page_url': next_page_url,
        'recipe_name': recipe_name
    })


from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import redirect, render

from .models import SavedRecipe, UserProfile


def user_pro(request):
    if request.method == 'POST':
        recipe_label = request.POST.get('recipe_label')
        recipe_url = request.POST.get('recipe_url')
        recipe_image = request.POST.get('recipe_image')
        meal_type = request.POST.get('meal_type')
        cuisine_type = request.POST.get('cuisine_type')
        source = request.POST.get('source')

        # Create a SavedRecipe instance
        saved_recipe = SavedRecipe.objects.create(
            recipe_label=recipe_label,
            recipe_url=recipe_url,
            recipe_image=recipe_image,
            meal_type=meal_type,
            cuisine_type=cuisine_type,
            source=source
        )

        # Associate the SavedRecipe instance with the current user's profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        user_profile.saved_recipes_savedrecipe.add(saved_recipe)

        # Redirect to the same view after successful submission
        return redirect('user_pro')

    # Fetch all saved recipes associated with the current user
    user_profile = UserProfile.objects.get(user=request.user)
    saved_recipes = user_profile.saved_recipes_savedrecipe.all()

    # Filtering and pagination
    queryset = saved_recipes

    if 'Search' in request.GET:
        recipe_name = request.GET.get('Search')
        queryset = queryset.filter(recipe_label__icontains=recipe_name)
        if not queryset:
            messages.error(request, "Recipe not found")

    paginator = Paginator(queryset, 3)  # Display 3 recipes per page
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'saved_recipes': saved_recipes,  # Pass the saved recipes to the template
        'queryset': page_obj,
    }

    return render(request, 'recipe/user_pro.html', context)
