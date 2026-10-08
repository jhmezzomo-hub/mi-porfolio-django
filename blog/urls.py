from . import views
from django.urls import path

urlpatterns = [
    path("", views.blog_index, name="blog_index"),
    path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),
    path("category/<category>/", views.blog_category, name="blog_category"),
]