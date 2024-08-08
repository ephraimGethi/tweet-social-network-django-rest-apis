from django.urls import path, re_path,include
from django.urls import path
from tweets.views import home_view,tweet_detail_view,tweet_list_view,create_tweet_view,tweet_delete_view,tweet_Action_view,tweet_feed_view
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('',home_view,name='home'),
    path('tweets',tweet_list_view,name='tweets'),
    path('tweetsfeed',tweet_feed_view,name='tweets'),
    path('tweets/<int:tweet_id>',tweet_detail_view,name='home'),
    path('tweetsdelete/<int:tweet_id>',tweet_delete_view,name='delete'),
    path('createtweet',create_tweet_view,name='createtweet'),
    path('tweetaction',tweet_Action_view,name='action'),

    path('auth/token',obtain_auth_token),

]