from django.urls import path
from . import views

# url routing
urlpatterns = [
    path("", views.index, name='index'),
    path("create/", views.create_post, name="create_post"),
    path('delete/<int:post_id>/', views.delete_post, name="delete_post")
]