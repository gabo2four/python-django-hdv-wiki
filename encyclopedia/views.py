
from asyncio.windows_events import NULL
from audioop import reverse
from django.urls import reverse
from django.shortcuts import  render
from django import forms
from . import util
from django.http import HttpResponseRedirect
import markdown as md
from random import randint

class NewPageForm(forms.Form):
    tittle = forms.CharField(label="Title")
    entry = forms.CharField(widget=forms.Textarea())

class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wikiTopic(req,tittle):
    return render(req,"encyclopedia/topic.html",{
        "tittle":tittle,
        "entrie":md.markdown(util.get_entry(tittle) or "")
    })

def buttonSearch(req):
    keyCode = 2
    lowerWordSearch = req.GET["q"].lower()
    listCoinci = []
    tittle = "The following matches were found:"
    entry = ""
    for x in util.list_entries():
        if x.lower() == lowerWordSearch:
            tittle = x
            entry = md.markdown(util.get_entry(tittle))
            keyCode = 1
        
        if keyCode == 2:
            for i in x:
                if req.GET["q"][0].lower() == i.lower():
                    cadenaStr = x[x.index(i):x.index(i)+len(req.GET["q"])].lower()
                    if cadenaStr == lowerWordSearch:
                        listCoinci.append(x)      
                        entry = listCoinci
                         
    if len(listCoinci) == 0 and keyCode == 2:
        keyCode = 0

    return render(req,"encyclopedia/searchTopic.html",{
        "tittle":tittle,
        "entries":entry,
        "keyCode":keyCode
    })

def newPage(req):
    warningMess = ""
    form = NewPageForm(req.POST)
    formKey = "yes"
    for x in util.list_entries():
        if req.POST.get('tittle') == x:
            formKey = "not"


    if req.method == "POST":
        if form.is_valid() and formKey == "yes" and req.POST.get('tittle'):
            title = form.cleaned_data["tittle"]
            entry = form.cleaned_data["entry"]
            util.save_entry(title,entry)
            return HttpResponseRedirect(reverse("index"))
        else:
            warningMess = "Title already registered"
            return render(req,"encyclopedia/newPageForm.html",{
                "form":form,
                "wM":warningMess
            })
            
    return render(req,"encyclopedia/newPageForm.html",{
        "form": NewPageForm(),
        "wM": warningMess
    })

def editPage(req,tittle):
    default_data = {
        'content':util.get_entry(tittle)
    }
    return render(req,"encyclopedia/editPageForm.html",{
        "form": EditPageForm(default_data),
        "tittle": tittle
    })

def saveEdit(req,tittle):
    prevChar = NULL
    print("REQ",req.POST)
    
    print(req.POST.get('content').replace("\r\n"," "))


    form = EditPageForm(req.POST)
    if req.method == "POST":
        if form.is_valid():
            content = form.cleaned_data["content"]
            listContent = list(content)
            for x in listContent:
                if x == "\r":
                    print("Si HAY")
                    print(listContent.index(x)+1)
                    prevChar = listContent.index(x)
                    listContent[listContent.index(x)] = ''
                elif prevChar:
                    if prevChar+2 == listContent.index(x) :
                        listContent[listContent.index(x)-2] = '\r'
                        listContent[listContent.index(x)-1] = '\n'
                        print("god")

                
                    


            
            print(listContent)
            finalContent = "".join(listContent)
            print(finalContent)
            util.save_entry(tittle,finalContent)
            return HttpResponseRedirect(reverse("wikiTopic",
                args=[tittle]
            ))


def randomPage(req):
    titlesList = util.list_entries()
    tittleIndex = randint(0,len(titlesList)-1)
    tittle = titlesList[tittleIndex]
    return HttpResponseRedirect(reverse("wikiTopic",
                args=[tittle]
            ))