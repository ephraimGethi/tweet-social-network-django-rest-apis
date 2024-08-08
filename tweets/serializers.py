from rest_framework import serializers
from .models import Tweet
from profiles.serializers import PublicProfileSerializer

TWEET_ACTION_OPTIONS = ['like','unlike','retweet']

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank = True,required = False)

    def validate_action(self,value):
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError('this is not a valid action for tweet')
        return value

class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only = True)
    class Meta:
        fields = ['user','content','likes']
        model = Tweet
    def get_likes(self,obj):
        return obj.likes.count()
    
    def validate_content(self, value):
        
        if len(value) > 240:
            raise serializers.validationError('this teet is too long')
        return value
    
class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField()
    id = serializers.IntegerField()

class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only = True)
    parent = TweetCreateSerializer(read_only = True)
    user = PublicProfileSerializer(source = 'user.profile',read_only = True)
    class Meta:
        fields = ['parent','user','content','likes','is_retweet']
        model = Tweet
    def get_likes(self,obj):
        return obj.likes.count()
    