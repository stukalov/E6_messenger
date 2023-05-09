from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class SaveAvatarMixin:
    def save(self):
        user = super().save()
        avatar = self.cleaned_data['avatar']
        if avatar is not None:
            profile = user.profile
            profile.avatar = avatar
            profile.save()
        return user


class SignupForm(SaveAvatarMixin, UserCreationForm):
    avatar = forms.ImageField(label='Аватар', required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2',
            'avatar',
        )


class UserUpdateForm(SaveAvatarMixin, forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'avatar'
        )


class SendMessage(forms.Form):
    text = forms.CharField(label='', widget=forms.Textarea)
