from django.contrib import admin
from . import views
from django.urls import path

app_name = 'blogapp'
urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),

]

