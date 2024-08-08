from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,JsonResponse
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
from rest_framework.decorators import api_view,permission_classes,authentication_classes,renderer_classes


from django.forms import model_to_dict

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication
from rest_framework.renderers import JSONRenderer
from django.db.models import Q
from django.contrib.auth import get_user_model

from ..models import Profile
from ..serializers import PublicProfileSerializer

User = get_user_model()

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def user_follow_view(request,username,*args,**kwargs):
    current_user = request.user
    to_follow_user = User.objects.filter(username=username)
    if to_follow_user.exists() == False:
        return Response({},status=404)
    other = to_follow_user.first()
    profile = other.profile
    
    action = request.data.get('action')
    if action == 'follow':
        profile.followers.add(current_user)
    elif action == 'unfollow':
        profile.followers.remove(current_user)
    else:
        pass

    current_followers_qs = profile.followers.all()
    return Response({"followers":current_followers_qs.count()},status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_detail_api_view(request,username):
    qs = Profile.objects.filter(user__username = username)
    if not qs.exists():
        return Response({"detail":"user not found"},status=404)
    profile_obj = qs.first()
    data = PublicProfileSerializer(profile_obj,many=False)
    return Response(data.data,status=200)