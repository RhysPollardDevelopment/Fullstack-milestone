from django.shortcuts import render


def all_recipes(request):
    template = "recipes/recipes.html"
    return render(request, template)
