from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown

from . import util

markdowner = Markdown()

# Create Entry class
class Entry():
    def __init__(self, title):
        self.title = title
        self.content = " "

# Add variable for initial values of entry titles
entries = ["CSS", "Django", "Git", "HTML", "Python"]


# Use django forms to generate fields for create page
class NewEntryForm(forms.Form):
    entry_title = forms.CharField(label="Title")
    entry_markdown = forms.CharField(widget=forms.Textarea)

#Define home page view
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Define create page view
def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data["entry_title"],
            entry_markdown = form.cleaned_data["entry_markdown"]
            return HttpResponseRedirect(reverse("encyclopedia:entry"), {
                "entry_title": title.capitalize()
            })
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })


    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })

#Define error page view
def error(request):
    return render(request, "encyclopedia/error.html")

#Define entry page view
def entry(request, title):
    entry_string = util.get_entry(title)
    error_message = "Could not find your file. Please try again."
    if entry_string:
        converted_md = markdowner.convert(entry_string)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "markdown": converted_md
        })
    else:
        return render(request, "encyclopedia/error.html", {
            "error_message": error_message
        }) 

#Define search page view
def search(request):
    return render(request, "encyclopedia/search.html")