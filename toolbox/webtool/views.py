from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import Tool, Favorite, Category, Review

# Create your views here.

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