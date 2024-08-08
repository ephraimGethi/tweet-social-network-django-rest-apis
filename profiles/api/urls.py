from django.urls import path
from .views import user_follow_view,profile_detail_api_view


urlpatterns = [
    path('<str:username>',user_follow_view ),
    path('<str:username>/detail',profile_detail_api_view ),
]
