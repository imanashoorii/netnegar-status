from django.urls import path
import netnegar.views as views

urlpatterns = [
    path('check/set/w3k8HNgh2RQNb62BnFIp9hb2ljJh36CpaTUV4d8XW3oIQReqTiYVNGbNjOFYdSso4cbNPfJViXBYfptGCFrXP/', views.NewRecord.as_view()),
    path('check/get/w3k8HNgh2RQNb62BnFIp9hb2ljJh36CpaTUV4d8XW3oIQReqTiYVNGbNjOFYdSso4cbNPfJViXBYfptGCFrXP/', views.GetData.as_view()),
]
