from django.urls import path
from .views import dashboard, user_logout, homepage, pag_login

urlpatterns = [
    path('login/', pag_login, name='login'),
    path('', homepage, name="homepage"),
    path('dashboard/', dashboard, name="dashboard"),
    path('logout/', user_logout, name="logout"),
]
