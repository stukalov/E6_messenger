from django import template
from messenger.models import *

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    return d.urlencode()


@register.simple_tag(takes_context=True)
def message_read(context, message, **kwargs):
    message.make_read()
    return ''


@register.simple_tag(takes_context=True)
def messages_total(context, sender, receiver, **kwargs):
    return Message.total(sender, receiver)


@register.simple_tag(takes_context=True)
def messages_unread(context, sender, receiver, **kwargs):
    return Message.unread(sender, receiver)
