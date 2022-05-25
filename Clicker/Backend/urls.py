from django.urls import path
from . import views
from .views import *

boosts = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('call_click/', call_click),
    path('boosts/', boosts, name='boosts')
]