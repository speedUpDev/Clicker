from django.urls import path
from . import views
from .views import *

boosts = views.BoostViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
lonely_boost = views.BoostViewSet.as_view({
    'put': 'partial_update',
})

urlpatterns = [
    path('', index, name='index'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('call_click/', call_click),
    path('boosts/', boosts, name='boosts'),
    path('update_coins/', views.update_coins),
    path('boost/<int:pk>/', lonely_boost, name='boost'),
    path('core/', views.get_core),
    path('rank/<int:pk>/', views.get_rank),
]