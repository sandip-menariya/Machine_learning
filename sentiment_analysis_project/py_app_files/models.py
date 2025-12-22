from django.db import models

# Create your models here.
class Sentiment(models.Model):
    comment=models.TextField()
    positive=models.FloatField()
    negative=models.FloatField()
    neutral=models.FloatField()
    compound=models.FloatField()
    create_time=models.DateTimeField(auto_now_add=True)

class PostSentiment(models.Model):
    username=models.TextField()
    userid=models.TextField()
    postid=models.TextField()
    post_title=models.TextField()
    sentiment=models.TextField()
    sentiment_index=models.FloatField()
    total_comments=models.IntegerField()
    pos_sum=models.FloatField()
    neg_sum=models.FloatField()
    neu_sum=models.FloatField()
    total_positive=models.IntegerField()
    total_negative=models.IntegerField()
    total_neutral=models.IntegerField()
