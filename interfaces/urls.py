from django.urls import path
from .views import dashboard, user_logout

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('logout/', user_logout, name="logout"),
]
