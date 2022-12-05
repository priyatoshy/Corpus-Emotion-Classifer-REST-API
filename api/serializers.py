from rest_framework import serializers
from notes.models import Note,Rating
from django.contrib.auth.models import User
from  rest_framework.response import Response

'''


Serializers in Django REST Framework are responsible for converting objects
into data types understandable by javascript and front-end frameworks. 
Serializers also provide deserialization, allowing parsed data to be converted back into complex types,
after first validating the incoming data


#just like model methods that can do compute with the internal data of
the model and can be used as a property,
we can also have serializer methods

'''

#user serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','groups']
        extra_kwargs = {'password': {'write_only': True}}

    #ovverrding the create functionality for password hashing
    #for accepting json data suitable passsword
    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user

#rating serializer
class RatingSerializer(serializers.ModelSerializer):
    reviewer=UserSerializer(many=False)
    class Meta:
        model=Rating
        fields="__all__"
#blog serializer
class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Note
        fields="__all__"
    #the writer field returns the object instead of the id
    #it is getting serialized in a nested way
    creator=UserSerializer(many=False)
    #the statement below triggers the get_rating method
    #it takes in the the serializer as self and the model as the obj
    #it then gets the chilf objects and serializes them and combines
    #them with the json data
    rating=serializers.SerializerMethodField()
    #getting all the comments of the posts in a serilized
    #format

    def get_rating(self,obj):
        rating=obj.rating_set.all()
        #print(f"{comments}")
        serializer=RatingSerializer(rating,many=True)
        #not returning a response because it is not going to
        #be a view
        return serializer.data
