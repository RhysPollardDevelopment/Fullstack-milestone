from django.http.response import BadHeaderError, HttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from .forms import ContactForm
from django.core.mail import send_mail


def index(request):
    """View which returns index page"""
    template = "customerservice/index.html"
    return render(request, template)


def contact(request):
    """View which returns index page"""
    if request.method == "POST":
        contact_form = ContactForm(request.POST)

        if contact_form.is_valid():
            subject = contact_form.cleaned_data["subject"]
            name = contact_form.cleaned_data["name"]
            customer_email = contact_form.cleaned_data["email_address"]
            body = contact_form.cleaned_data["body"]
            # Included name in Subject so any response can be more personal.
            try:
                send_mail(
                    f"{subject} from {name}",
                    body,
                    customer_email,
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
            # https://docs.djangoproject.com/en/3.2/topics/email/
            # user of errors for email from aboce django doc.
            except BadHeaderError:
                return HttpResponse("Invalid header found")
            return redirect("contact_success")
    else:
        contact_form = ContactForm()

    context = {
        "API_KEY": settings.GOOGLE_API_KEY,
        "contact_form": contact_form,
    }
    template = "customerservice/contact.html"
    return render(request, template, context)


def contact_success(request):
    """Success page on contact form message used."""
    template = "customerservice/contact_thanks.html"
    return render(request, template)


def about(request):
    """View which returns index page"""
    template = "customerservice/about.html"
    return render(request, template)
