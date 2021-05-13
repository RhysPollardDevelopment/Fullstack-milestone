from django.shortcuts import render, redirect, reverse, get_object_or_404
from .models import UserProfile, User


def profiles(request):
    """
    Returns page which contains all current products for the subscription
    service.
    """
