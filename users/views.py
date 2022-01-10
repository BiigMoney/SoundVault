from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.views.generic import View, ListView
from soundboard.models import Sound
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class SettingsView(View, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        form = UserUpdateForm(instance=request.user)

        context = {
            "form": form
        }

        return render(request, 'users/settings.html', context)

    def post(self, request, *args, **kwargs):
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has successfully been updated.')
            return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, 'users/settings.html', context)

class ProfileView(ListView):
    model = Sound
    template_name = 'users/profile.html'
    context_object_name = "sounds"
    ordering = ['-id']
    paginate_by = 12

    def get_context_data(self, **kwargs):
        pk = self.kwargs['pk']
        user = User.objects.get(pk=pk)
        sounds = Sound.objects.filter(uploader=user)
        likes = 0
        for sound in sounds:
            likes+=sound.likes.count()
        context  = super().get_context_data(**kwargs)
        context['user'] = user
        context['sound_count'] = len(sounds)
        context['like_count'] = likes
        return context

    def get_queryset(self):
        return Sound.objects.filter(uploader=User.objects.get(pk=self.kwargs['pk'])).order_by('-id')
