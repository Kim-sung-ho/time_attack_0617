from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # CBV 는 as_view 를 적어줘야한다.
    path('user/', views.UserView.as_view()),
    path('login/', views.UserAPIView.as_view()),
]
