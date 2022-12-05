from django.http import JsonResponse
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from  rest_framework.response import Response
from .serializers import NoteSerializer,RatingSerializer,UserSerializer
from notes.models import Note,Rating
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from django.http import QueryDict
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
'''
Function Based View
@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def get_random(request):
    queryset=Note.objects.all()
    data=queryset.first()
    data.analyse
    print(data.analysis)
    serializer=NoteSerializer(queryset,many=True)
    return Response(serializer.data)

'''
#notes api

#login API
class LoginApi(APIView):

    def post(self,request):
        if request.user.is_authenticated:
            return Response({"Status":404})
        else:
            #try:
                data=request.POST
                username=data["username"]
                password=data["password"]
                user=authenticate(username=username,password=password)
                if user is None:
                    return Response({"status":404})
                else:
                     serializer=UserSerializer(user,many=False)
                     refresh=RefreshToken.for_user(user)
                     data={
                            "data":serializer.data,
                            "access":str(refresh.access_token),
                        }
                     return Response(data)  
            #except:
                #return Response({"status":404})
#logout

#login API
class LogoutApi(APIView):

    def post(self,request):
        user=request.user
        if request.user.is_authenticated:
            user.logout()
        else:
            return Response({"status":404})
           

#logoutAPI
class MyNote(APIView):
    #if using drf
    #authentication_classes=[TokenAuthentication]
    #else
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        notes=Note.objects.all()
        data=notes.first()
        data.analyse
        print(data.analysis)
        serializer=NoteSerializer(notes,many=True)
        return Response(serializer.data)
    def post(self,request):
        user=request.user
        topic=request.POST["topic"]
        note=request.POST["note"]
        image=request.FILES["featured_image"]
    
        sid_obj= SentimentIntensityAnalyzer()
        emotion=sid_obj.polarity_scores(note)
    
        note=Note.objects.create(creator=user,topic=topic,note=note,emotion=emotion,featured_image=image)

    
        serializer=NoteSerializer(note,many=False)
        return Response(serializer.data)

    def put(self,request):
        pk=request.POST["pk"]
        
        note1=Note.objects.get(id=pk)

        if request.user==note1.creator:
        
            note=request.POST["note"]
     
    
            sid_obj= SentimentIntensityAnalyzer()
            emotion=sid_obj.polarity_scores(note)
    
          
            note1.note=note
            note1.featured_image=request.FILES["featured_image"]
            note1.emotion=emotion
            note1.save()


    
            serializer=NoteSerializer(note1,many=False)
            return Response(serializer.data)
        else:
            return Response({"Status":"Forbidden Request"})

    def delete(self,request):
        pk=request.POST["pk"]
        
        note1=Note.objects.get(id=pk)

        if request.user==note1.creator:
            note1.delete()
            return Response({"Status":"Success"})
        else:
            return Response({"Status":"Forbidden Request"})

       
    
        
        
class UserRegistration(APIView):
    #if using drf
    #authentication_classes=[TokenAuthentication]
    #else

    #authentication_classes=[JWTAuthentication]
    #permission_classes=[IsAuthenticated]
    def post(self,request):
        if request.user.is_authenticated==False:
            username=request.POST["username"]
            password=request.POST["password"]
            if username:
                if password:
                    user=User.objects.filter(username__exact=username)
                    if user:
                        return Response({"Status":404})
                    else:
                        user=User.objects.create(username=username,password=password)
                        serilizer=UserSerializer(user,many=False)
                        #for drf token
                        #token_obj,status=Token.objects.get_or_create(user=user)
                        #for jwt
                        refresh=RefreshToken.for_user(user)
                        data={
                            "data":serilizer.data,
                            "access":refresh.access_token,
                        }
                        return Response(serilizer.data)
                else:
                    return Response({"Status":404})
            else:
                return Response({"Status":404})
        else:
            return Response({"Status":404})





'''

When you send form-encoded data, whether it's POST or PUT, in Django you always find the parameters in request.POST. So you would find your data in request.POST['conid'].

However, you are not sending form-encoded data; you are sending JSON. You need to access the request body, and pass it to the json.loads function to decode:

def kill(request):
  data = json.loads(request.body)
  conid = data['connid']

'''

#it basically creates a crud operation function with the Model.Viewset
#using a class based view
'''
class Noteviewset(viewsets.ModelViewSet):
    queryset=Note.objects.all()
    serializer_class=NoteSerializer
'''
'''
With the viewset and Modelviewset class based view we can
automatically get the get post put delete and get single 
model view
api/notes get post
api/notes/id -get single delete update


'''

#DRF TOKENS
#JWT TOKENS
#PASSWORD HASHING
#LOGIN 
#USER REGISTRATION
#LOGOUT
#GENERIC VIEWS
#EXCEL
#LOGOUT
#PUT VS POST
class MyRating(APIView):
    #if using drf
    #authentication_classes=[TokenAuthentication]
    #else
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def get(self,request):
        ratings=Rating.objects.all()
        serializer=RatingSerializer(ratings,many=True)
        return Response(serializer.data)

    def post(self,request):
        pk=request.POST["pk"]
        
        note=Note.objects.get(id=pk)
        user=request.user
        
        score=request.POST["score"]
        reviewer=user
    

        try:
            rating=Rating.objects.create(reviewer=reviewer,note=note,score=score)
            serializer=RatingSerializer(rating,many=False)
            return Response(serializer.data)
        except:
            return Response({"Error":500})
    
        
    def delete(self,request):
        pk=request.POST["pk"]
        
        rating=Rating.objects.get(id=pk)

        if request.user==rating.reviewer:
            rating.delete()
            return Response({"Status":"Success"})
        else:
            return Response({"Status":"Forbidden Request"})


    