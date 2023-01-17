from django.urls import path
import netnegar.views as views

urlpatterns = [
    path('check/set/0/', views.NewRecord.as_view()),
    path('check/get/0/', views.GetData.as_view()),
]
