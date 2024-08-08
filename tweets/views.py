from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from rest_framework.decorators import api_view,permission_classes,authentication_classes,renderer_classes


from .models import Tweet
from django.forms import model_to_dict
from .forms import TweetForm
from .serializers import (TweetSerializer,
                          TweetActionSerializer,
                          TweetCreateSerializer)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.renderers import JSONRenderer
from django.db.models import Q

from rest_framework.pagination import PageNumberPagination

ALLOWED_HOSTS = settings.ALLOWED_HOSTS
# Create your views here.
def home_view(request):
    return render(request,'pages/home.html')

def tweet_list_view_pure_django(request,*args,**kwargs):
    qs = Tweet.objects.all()
    tweet_list = [{"id":x.id,"content":x.content} for x in qs]
    data = {"response":tweet_list}
    return JsonResponse(data)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_tweet_view(request,*args,**kwargs):
    data = request.data
    serializer = TweetCreateSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user = request.user)
        return Response(serializer.data)
    
@api_view(['GET'])
def tweet_list_view(request):
    qs = Tweet.objects.all()
    username = request.GET.get('username')
    if username != None:
        qs = qs.filter(user__username__iexact = username)
    data = TweetSerializer(qs,many = True).data
    res = {
        "data":data
    }
    return Response(res)
from django.db.models import Q
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tweet_feed_view(request):
    paginator = PageNumberPagination()
    paginator.page_size = 5
    user = request.user
    qs = Tweet.objects.feed(user)
    paginated_qs = paginator.paginate_queryset(qs,request)
    
    data = TweetSerializer(paginated_qs,many = True).data
    return paginator.get_paginated_response(data)

@api_view(['GET'])
def tweet_detail_view(request,tweet_id,*args,**kwargs):
    qs = Tweet.objects.filter(id=tweet_id)
    data = TweetSerializer(qs,many = True).data
    user = str(request.user.email)
    res = {
        "Logged is user is":user,
        "data":data
    }
    return Response(res)

@api_view(['GET','DELETE'])
def tweet_delete_view(request,tweet_id,*args,**kwargs):
    qs = Tweet.objects.get(id=tweet_id)
    if request.method == 'GET':
      data = TweetSerializer(qs,many = False).data
      return Response(data)
    else:
        qs.delete()
        return Response('deleted successfuly')
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_Action_view(request):

    serializer = TweetActionSerializer(data = request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
        content = data.get("content")
    qs = Tweet.objects.get(id = tweet_id)
    if not qs.DoesNotExist():
        return Response({},status=404)
    obj = qs
    data2 = {
        "id":serializer.validated_data.get('id'),
        "action":serializer.validated_data.get('action')
    }
    if action == 'like':
        obj.likes.add(request.user)
    elif action == 'unlike':
        obj.likes.remove(request.user)
    elif action == 'retweet':
        parent_obj = obj
        Tweet.objects.create(user = request.user,
                                         parent = parent_obj,
                                         content = content)
    else:
        pass
    return Response(data2)


def create_tweet_view_pure_django(request,*args,**kwargs):
    form = TweetForm(request.POST or None)
    next_url = '/'
    if form.is_valid():
        obj = form.save()
        obj.save()
        if next_url != None and url_has_allowed_host_and_scheme(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    return render(request,'components/forms.html',context={"form":form})
def tweet_detail_view_pure_django(request,tweet_id,*args,**kwargs):
    data = {
        "id":tweet_id,
    }
    status = 200
    try:
        obj = Tweet.objects.get(id = tweet_id)
        data['content'] = obj.content
    except:
        data['message'] = 'not found'
        status = 404
    # data = model_to_dict(obj,fields=['content','id'])
    return JsonResponse(data,status=status)