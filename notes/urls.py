from django.urls import path 
from . import views
#imporing path 
#import views file from its own directory

#creating an url configuration/URLConf
from .views import Home

urlpatterns = [
    path('',Home.as_view(),name='home'),
]

