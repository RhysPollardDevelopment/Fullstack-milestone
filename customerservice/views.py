from django.shortcuts import render


def index(request):
    """View which returns index page"""
    return render(request, "customerservice/index.html")


def contact(request):
    """View which returns index page"""
    return render(request, "customerservice/contact.html")


def about(request):
    """View which returns index page"""
    return render(request, "customerservice/about.html")
