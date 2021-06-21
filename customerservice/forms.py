from django import forms


class ContactForm(forms.Form):

    name = forms.CharField(label="Name", max_length=100)
    email_address = forms.EmailField(max_length=40)
    subject = forms.CharField(max_length=80)
    body = forms.CharField(
        max_length=400, widget=forms.Textarea(attrs={"rows": 4, "cols": 20})
    )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "name": "Name",
            "email_address": "Email",
            "subject": "Subject",
            "body": "Message",
        }

        for field in self.fields:
            placeholder = f"{placeholders[field]}"
            self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "form-input"
            self.fields[field].label = False
