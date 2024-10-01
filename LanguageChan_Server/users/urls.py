from django.urls import path
from .views import *

urlpatterns = [
    path('loginout/', Loginout.as_view()),
    path('signupdown/', Signupdown.as_view()),
    path('charas/', UsersCharasView.as_view()),
    path('chara/', UsersCharaView.as_view()),
    path('friends/', UsersFriendsView.as_view()),
    path('item/', UsersItemView.as_view()),
    path('progress/', UsersProgressView.as_view())
]