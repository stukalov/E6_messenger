from django.urls import path
from .views import *


messenger_urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('signup', SignUpView.as_view(), name='messenger.signup'),
    path('user/<int:pk>/update', UserUpdate.as_view(), name='messenger.user.update'),
    path('users', UserList.as_view(), name='messenger.users'),
    path('user/<int:pk>', UserView.as_view(), name='messenger.user.view'),
    path('messages/<int:sender>/<int:receiver>', Messages.as_view(), name='messenger.messages'),
]