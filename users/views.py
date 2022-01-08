from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.views.generic import View
from soundboard.models import Sound
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Welcome {username}! Your account has successfully been created. You may now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        user = User.objects.get(pk=pk)
        sounds = Sound.objects.filter(uploader=user)
        likes = 0
        for sound in sounds:
            likes+=sound.likes.count()
        context = {
            'sounds': sounds,
            'user': user,
            'sound_count': len(sounds),
            'like_count': likes,

        }

        return render(request, 'users/profile.html', context)
