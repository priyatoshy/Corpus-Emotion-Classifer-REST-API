from django.db import models
import uuid
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.
class Note(models.Model):
    creator=models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    topic=models.CharField(max_length=50)
    featured_image=models.ImageField(blank=True,null=True)
    note=models.TextField(max_length=5000)
    emotion=models.JSONField(null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True,null=True,blank=True)


    def __str__(self):
        return self.topic

    #model method
    @property
    def analyse(self):

        sid_obj= SentimentIntensityAnalyzer()
        analysis=sid_obj.polarity_scores(self.note)
        self.analysis=analysis

class Rating(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    reviewer=models.ForeignKey(User,on_delete=models.CASCADE)
    note=models.ForeignKey('Note',on_delete=models.CASCADE)
    score=models.FloatField(default=0.0,validators=[MinValueValidator(0),MaxValueValidator(10)])
    created=models.DateTimeField(auto_now_add=True,null=True,blank=True)

    class Meta:
        unique_together = [['reviewer', 'note']]
        
    def __str__(self):
        return self.reviewer



  
    