from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.views.generic import ListView, TemplateView, CreateView, UpdateView, DetailView, View
from django.views.generic.edit import FormMixin
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin
from django.db.models import Q

from .forms import *
from .models import *


def index_page(request):
    return HttpResponseRedirect(reverse('main_page'))


class MainPage(TemplateView):
    template_name = 'default.html'


class SignUpView(AccessMixin, CreateView):
    model = User
    form_class = SignupForm
    template_name = 'registration/signup.html'

    def post(self, request, *args, **kwargs):
        result = super().post(request, *args, **kwargs)
        return result

    def get_success_url(self):
        user = self.object
        url = reverse('messenger.user.update', kwargs={'pk': user.pk})
        return url

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserUpdate(AccessMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'registration/update.html'

    def get_success_url(self):
        user = self.object
        url = reverse('messenger.user.update', kwargs={'pk': user.pk})
        return url

    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class UserList(LoginRequiredMixin, ListView):
    model = User
    template_name = 'user_list.html'
    ordering = 'username'
    context_object_name = 'users'
    paginate_by = 50


class UserView(LoginRequiredMixin, FormMixin, DetailView):
    model = User
    form_class = SendMessage
    template_name = 'user_item.html'
    context_object_name = 'message_user'

    def init(self, request):
        self.request = request
        self.sender = request.user
        self.receiver = self.get_object()

    def get(self, request, *args, **kwargs):
        self.init(request)
        return super(UserView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.init(request)
        form = self.get_form()
        if form.is_valid():
            self.save_message(form)
        return super(UserView, self).get(request, *args, **kwargs)

    def save_message(self, form):
        Message.objects.create(sender=self.sender, receiver=self.receiver, text=form.cleaned_data['text'])

    def get_messages(self):
        condition = Q(sender=self.sender, receiver=self.receiver)
        condition |= Q(sender=self.receiver, receiver=self.sender)
        return Message.objects.filter(condition).order_by('created')

    def get_context_data(self, **kwargs):
        result = super(UserView, self).get_context_data(**kwargs)
        result |= {
            'receiver': self.receiver,
            'sender': self.sender,
            'messages': self.get_messages(),
            'url': reverse('messenger.messages', kwargs={
                'sender': self.sender.pk,
                'receiver': self.receiver.pk,
            }),
        }
        return result

    def get_success_url(self):
        return reverse('messenger.user.view', kwargs={'pk': self.receiver.pk})


class Messages(View):

    def get(self, request, *args, **kwargs):
        last_id = request.GET.get('id')
        unread_id = request.GET.get('unread')
        unread = unread_id.split(',') if unread_id else None
        sender = User.objects.get(pk=kwargs['sender'])
        receiver = User.objects.get(pk=kwargs['receiver'])
        condition = Q(sender=sender, receiver=receiver)
        condition |= Q(sender=receiver, receiver=sender)
        if last_id or unread:
            if last_id and unread:
                condition &= Q(id__gt=last_id) | Q(id__in=unread)
            elif last_id:
                condition &= Q(id__gt=last_id)
            else:
                condition &= Q(id__in=unread)
        messages = Message.objects.filter(condition).order_by('created')
        context = {
            'messages': messages,
            'sender': sender,
            'receiver': receiver,
            'empty': False,
        }
        return render(request, 'messages.html', context)
