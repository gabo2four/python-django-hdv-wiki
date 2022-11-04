from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:tittle>", views.wikiTopic, name="wikiTopic"),
    path("search/", views.buttonSearch, name="buttonSearch"),
    path("newPage/", views.newPage, name="newPage"),
    path("editPage/<str:tittle>", views.editPage, name="editPage"),
    path("savePage/<str:tittle>", views.saveEdit, name="saveEdit"),
    path("randomPage/", views.randomPage, name="randomPage"),

]
