from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


from .models import Tweet
User = get_user_model()

class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='kamau',password='adminadmin')
        Tweet.objects.create(content='my first tweet',user = self.user)
        Tweet.objects.create(content='my second tweet',user = self.user)
        Tweet.objects.create(content='my third tweet',user = self.user)
    def test_user_exists(self):
        user = User.objects.get(username = 'kamau')
        self.assertEqual(user.username,'kamau')

    def test_tweet_created(self):
        tweet_obj = Tweet.objects.create(content='my fouth tweet',user = self.user)
        self.assertEqual(tweet_obj.id,4)
        self.assertEqual(tweet_obj.user,self.user)
    
    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username,password = 'adminadmin')
        return client
    
    def test_tweet_list(self):
        client = self.get_client()
        response = client.get('/tweets')
        self.assertEqual(response.status_code,200)
        print(response.json())
        
    def test_action_like(self):
        client = self.get_client()
        response = client.post('/tweetaction',{"id":1,"action":"like"})
        self.assertEqual(response.status_code,200)
        print(response.json())

