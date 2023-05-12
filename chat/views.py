import json
from django.urls import reverse_lazy
from django.http import *
from django.views.generic import *
from django.views.generic.detail import *
from django.contrib.auth.mixins import *
from .models import *


class ChatList(LoginRequiredMixin, ListView):
    raise_exception = True
    model = ChatRoom
    template_name = 'chat_list.html'
    context_object_name = 'chats'
    paginate_by = 50


class ChatEdit(LoginRequiredMixin, DetailView):
    raise_exception = True
    model = ChatRoom
    template_name = 'chat_edit.html'
    context_object_name = 'chat_room'
    extra_context = {'ajax_url': reverse_lazy('chat.ajax')}

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is None:
            return ChatRoom()
        else:
            return super().get_object(queryset)


class AjaxView(AccessMixin, View):
    raise_exception = True
    permission_denied_message = 'Изменять чат может только его создатль'

    def __init__(self):
        self.object = None

    def send(self):
        result = self.object.__dict__.copy()
        del result['_state']
        result['room_url'] = self.object.get_room_url
        return JsonResponse(result)

    def get(self):
        return self.send()

    def post(self, request):
        if request.content_type != 'application/json':
            raise Http404()
        if self.object.admin != request.user:
            return self.handle_no_permission()
        self.object.__dict__.update(json.loads(request.body))
        self.object.save()
        return self.send()

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        object_id = self.kwargs.get('pk')
        if object_id is not None:
            self.object = ChatRoom.objects.get(pk=int(object_id))
        else:
            self.object = ChatRoom(admin=request.user)
        return super().dispatch(request, *args, **kwargs)


class Chat(LoginRequiredMixin, DetailView):
    model = ChatRoom
    template_name = 'chat_room.html'
    context_object_name = 'chat_room'
