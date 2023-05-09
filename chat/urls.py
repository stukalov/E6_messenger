from django.urls import path
from .views import *


chat_urlpatterns = [
    path("room/<int:pk>/", Chat.as_view(), name="chat.room"),
    path('list', ChatList.as_view(), name="chat.list"),
    path('edit', ChatEdit.as_view(), name="chat.new"),
    path('edit/<int:pk>', ChatEdit.as_view(), name="chat.edit"),
    path('ajax', AjaxView.as_view(), name="chat.ajax"),
    path('ajax/<int:pk>', AjaxView.as_view(), name="chat.ajax"),
]
