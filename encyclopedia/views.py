from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import markdown2
from random import randint

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    entry = util.get_entry(title)
    if not entry:
        return render(request, "encyclopedia/error.html", {
            "message": "Requested page not found!"
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": markdown2.markdown(entry)
    })
    

def search(request):
    title = request.POST['title']
    entry = util.get_entry(request.POST['entry'])
    if not entry:
        match = []
        titles = util.list_entries()
        for t in titles:
            if title.lower() in t.lower():
                match.append(t)
        return render(request, "encyclopedia/search.html", {
            "match": match,
            "search_term": title
        })

    else:
        return HttpResponseRedirect(reverse("title", args=[title]))

def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    else:
        title = request.POST["title"]
        text = request.POST["text"]
        for i in util.list_entries():
            if title.lower() == i.lower():
                return render(request, "encyclopedia/error.html", {
                    "message": "Title already exists!"
                })
        util.save_entry(title, text)
        return HttpResponseRedirect(reverse("title", args=[title]))

def edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        edited = request.POST["edit"]
        if edited == "false":
            content = util.get_entry(title)
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": content
            })
        else:
            content = request.POST["text"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("title", args=[title]))
    else:
        return HttpResponseRedirect(reverse("index"))

def random(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries) - 1)]
    return HttpResponseRedirect(reverse("title", args=[title]))
