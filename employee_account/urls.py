from django.urls import path
from .views import *


urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', MyProfile.as_view(), name='my-profile'),
]

