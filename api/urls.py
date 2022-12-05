from . import views
from django.urls import path,include
from rest_framework import routers
#from .views import Noteviewset
from .views import MyNote,UserRegistration,MyRating,LoginApi,LogoutApi
'''
router = routers.SimpleRouter()
#registering the class based views in the roter

router.register('notes',Noteviewset)


from rest_framework import routers
router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'accounts', AccountViewSet)
urlpatterns = router.urls
#path('',include(router.urls)),
'''

urlpatterns = [
    
    path('my-notes',views.MyNote.as_view()),
    path('my-ratings',views.MyRating.as_view()),
    path('register',views.UserRegistration.as_view()),
    path('login',views.LoginApi.as_view()),
    path('logout',views.LogoutApi.as_view()),
]