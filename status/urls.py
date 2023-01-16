from django.urls import path
from .user import UserMe
from .views import CreateIncident, ListIncident, DeleteIncident, OngoingIncident, UpdateIncident, HealthChart

urlpatterns = [
    path('user/u/me', UserMe.as_view()),
    path('incident/create', CreateIncident.as_view()),
    path('incident/list', ListIncident.as_view()),
    path('incident/<str:id>/delete', DeleteIncident.as_view()),
    path('incident/ongoings/', OngoingIncident.as_view()),
    path('incident/<str:id>/update', UpdateIncident.as_view()),

    #  Status Page
    path('detail/', HealthChart.as_view()),
]
