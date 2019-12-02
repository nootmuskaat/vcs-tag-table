from django.urls import path

from . import views

app_name = "tagtable"
urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.UploadTag.as_view(), name="upload"),
    path("list/", views.TagList.as_view(), name="list"),
    path("tag/<name>/", views.FetchTag.as_view(), name="detail"),
    path("tag/<name>/broken/", views.tag_broken, name="tag_broken"),
    path("tag/<name>/unbroken/", views.tag_unbroken, name="tag_unbroken"),
    path("branch/<name>/obsolete/", views.branch_obsolete, name="branch_obsolete"),
]
