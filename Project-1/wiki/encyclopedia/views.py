from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from markdown2 import Markdown
import random
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

# Create a separate Edit form to allow only edit of textarea 
class EditEntryForm(forms.Form):
    entry_markdown = forms.CharField(widget=forms.Textarea)

#Define home page view
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

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

#Define edit page view
def edit_page(request, title):
    content = util.get_entry(title)
    print(content)
    
    form = EditEntryForm(request.POST or None, initial={'entry_markdown': util.get_entry(title)})
    if form.is_valid():
        entry_markdown = form.cleaned_data["entry_markdown"]
        util.save_entry(title, entry_markdown)
        converted_md = markdowner.convert(entry_markdown)
        return render(request, "encyclopedia/entry.html", {
            "title": title.capitalize(),
            "markdown": converted_md
        })
    else:
        # form.fields['entry_markdown'].initial = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title
        })

#Define create page view
def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["entry_title"]
            entry_markdown = form.cleaned_data["entry_markdown"]
            print(title)
            if title == util.get_entry(title):
                raise ValidationError(f"This title already exists")
            util.save_entry(title, entry_markdown)
            # return HttpResponseRedirect(reverse(entry, args=(title,)))
            converted_md = markdowner.convert(entry_markdown)
            return render(request, "encyclopedia/entry.html", {
                "title": title.capitalize(),
                "markdown": converted_md
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


#Define random page view
def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    entry_string = util.get_entry(title)
    converted_md = markdowner.convert(entry_string)
    # return HttpResponseRedirect(reverse('random', args=(random_page,)))
    return render(request, "encyclopedia/random.html", {
                "title": title.capitalize(),
                "markdown": converted_md
            })

#Define search page view
def search(request):
    q = request.GET.get('q', '')
    entry_string = util.get_entry(q)
    if q is None:
        return render(request, 'encyclopedia/error.html')
    elif entry_string != None:
        converted_md = markdowner.convert(entry_string)
        return render(request, "encyclopedia/entry.html", {
            "title": q.capitalize(),
            "markdown": converted_md
        })
    else:
        sub_string = []
        for title in util.list_entries():
            if q in title:
                sub_string.append(title)

        return render(request, "encyclopedia/search.html", {
            "entries": sub_string
        })