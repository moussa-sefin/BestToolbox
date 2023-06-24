from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Tool, Favorite, Category, Review
from django.views.generic import View
from django.urls import reverse_lazy


# Create your views here.

def home_for_anonymouse_user(request):
    tools = Tool.objects.all()
    favorites = ""
    categories = Category.objects.all()
    reviews = ""
    ctx = {"tools":tools, "favorites":favorites, "categories":categories, "reviews":reviews}
    return render(request, "webtool/anonymous_user_index.html", ctx)

def tool_detail_for_anonymous_user(request, pk):
    tool = get_object_or_404(Tool, id=pk)
    reviews = ""
    favorites = ""
    categories = Category.objects.all()
    ctx = {'tool': tool, "favorites":favorites, "categories":categories, "reviews":reviews}
    return render(request, 'webtool/tool_detail_for_anonymous_user.html', ctx)

def home(request):
    tools = Tool.objects.all()
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    categories = Category.objects.all()
    reviews = Review.objects.filter(user=user) 
    ctx = {"tools":tools, "favorites":favorites, "categories":categories, "reviews":reviews}
    return render(request, "webtool/index.html", ctx)

def tool_details(request, pk):
    tool = get_object_or_404(Tool, id=pk)
    user = request.user
    favorites = Favorite.objects.filter(user=user)
    categories = Category.objects.all()
    reviews = Review.objects.filter(user=user, tool=tool)
    ctx = {'tool': tool, "favorites":favorites, "categories":categories, "reviews":reviews}
    return render(request, 'webtool/toolDetail.html', ctx)

class AddToFavolite(View):
    def get(self, request, pk):
        success_url = reverse_lazy('home')
        user = request.user
        tool = Tool.objects.get(id=pk)
        if Favorite.objects.filter(tool=tool, user=user).exists():
            print("not Added")
        else:
            favolite = Favorite.objects.create(user=user, tool=tool)
            favolite.save()
            print("added")
        return redirect(success_url)
    
def removeFromFavolite(request, pk):
    success_url = reverse_lazy('home')
    favorite = Favorite.objects.get(id=pk)
    favorite.delete()
    return redirect(success_url)
