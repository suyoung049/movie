from django.urls import path
from . import views

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:pk>/", views.detail, name="detail"),
    path("create/", views.create, name="create"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/comment_create/", views.comment_creat, name="comment_create"),
    path(
        "<int:article_pk>/comment/<int:comment_pk>/delete/",
        views.comment_delete,
        name="comment_delete",
    ),
    path(
        "<int:article_pk>/comment/<int:comment_pk>/update/",
        views.comment_update,
        name="comment_update",
    ),
]
