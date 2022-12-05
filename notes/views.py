from django.shortcuts import render,redirect,HttpResponse
from django.views import View



#class bases views
class Home(View):
    #method ->get
    def get(self,request):
        return HttpResponse("<h1>Succesful<h1>")