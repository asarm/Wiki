from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django import forms
from django.urls import reverse

from . import util
import random
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry title", widget=forms.TextInput(attrs={'class' : 'form-control col-md-8 col-lg-6','placeholder':'Title'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class' : 'form-control col-md-8 col-lg-8', 'rows' : 10,
                                                           'placeholder':'#Sample header\n\nSample content.'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def detail(request,name):
    markdowner = Markdown()

    if util.get_entry(name):
        entry = util.get_entry(name)
        context={
            "title":name,
            "entry":markdowner.convert(entry)
        }
    else:
        return render(request,"encyclopedia/not_Exist_error.html",{'title':name})
    return render(request,"encyclopedia/detail.html",context)

def random_entry(request):
    markdowner = Markdown()
    list = util.list_entries()
    rand = random.randint(0,len(list))
    title = list[rand-1]
    context={
        "title":title,
        "entry": markdowner.convert(util.get_entry(title))
    }
    return render(request,"encyclopedia/random.html",context)

def create(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None:
                util.save_entry(title,content)
                markdowner = Markdown()
                entry = util.get_entry(title)
                page = markdowner.convert(entry)
                context={
                    'title':title,
                    'entry':page
                }
                return redirect(f'wiki/{title}',context=context)
            else:
                return render(request, "encyclopedia/exist_error.html",{'title':title})

    else:
        form = NewEntryForm(request.POST)
        return render(request,"encyclopedia/create.html",{'form':form})

def edit(request,entryTitle):
    entryPage= util.get_entry(entryTitle)
    if entryPage is None:
        return render(request,'encyclopedia/not_Exist_error.html',{'title':entryTitle})
    form = NewEntryForm()
    form.fields["title"].initial = entryTitle
    form.fields["title"].widget = forms.HiddenInput()
    form.fields["content"].initial = entryPage
    if request.method == "POST":
            form = NewEntryForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse('detail', kwargs={'name':entryTitle}))
    else:
        return render(request, "encyclopedia/edit.html", {
                "form": form,
                "entryTitle": form.fields["title"].initial
            })


def search(request):
    value = request.GET.get('q','')
    if(util.get_entry(value) is not None):
        return HttpResponseRedirect(reverse("detail", kwargs={'name': value }))
    else:
        subStringEntries = []
        for entry in util.list_entries():
            if value.upper() in entry.upper():
                subStringEntries.append(entry)

    if len(subStringEntries) == 0:
        return render(request,'encyclopedia/not_Exist_error.html',{'title':value})
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": subStringEntries,
        "value": value
    })

