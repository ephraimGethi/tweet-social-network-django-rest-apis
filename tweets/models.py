from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q
User = settings.AUTH_USER_MODEL


# Create your models here.
class TweetLike(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    Tweet = models.ForeignKey("Tweet",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class TweetQueryset(models.QuerySet):
    def feed(self,user):
        profiles_exists = user.following.exists()
        followed_users_id = []
        if profiles_exists:
           followed_users_id = user.following.values_list("user__id",flat = True)
    
        return self.filter(Q(user__id__in = followed_users_id)
                                | Q(user = user)).distinct().order_by('-timestamp')
class TweetManager(models.Manager):
    def get_queryset(self):
        return TweetQueryset(self.model,using=self._db)
    
    def feed(self,user):
        return self.get_queryset().feed(user) 
    

class Tweet(models.Model):
    #handle retweet
    parent = models.ForeignKey("self",on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1,related_name="tweets")
    likes = models.ManyToManyField(User,related_name='tweet_user',blank=True,through=TweetLike)
    content = models.TextField(blank=True,null=True)
    image = models.FileField(upload_to='images/',blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    objects = TweetManager()

    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent != None
