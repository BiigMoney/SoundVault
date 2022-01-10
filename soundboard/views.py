from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, DeleteView, View
from django.http import HttpResponseRedirect
from .models import Sound
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User


class SoundListView(ListView):
    model = Sound
    template_name = 'soundboard/home.html'
    context_object_name = "sounds"
    ordering = ['-createdAt']
    paginate_by = 20


class SoundDetailView(DetailView):
    model = Sound
    template_name = 'soundboard/sound-detail.html'
    context_object_name = 'sound'

    def get_context_data(self, **kwargs):
        context = super(SoundDetailView, self).get_context_data(**kwargs)
        context['detail'] = True
        return context 


class SoundCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = Sound
    template_name = 'soundboard/add_sound.html'
    fields = ['name', 'soundFile']

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)


class SoundDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Sound

    def test_func(self):
        return self.request.user == self.get_object().uploader


    def get_success_url(self):
        return self.request.POST.get('next', '/')


class LikeView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        return HttpResponseRedirect('/')

    def post(self, request, pk, *args, **kwargs):
        sound = Sound.objects.get(pk=pk)

        liked = False

        for like in sound.likes.all():
            if like == request.user:
                sound.likes.remove(request.user)
                liked = True

        if not liked:
            sound.likes.add(request.user)

        redirect = request.POST.get('next', '/')
        return HttpResponseRedirect(redirect)

def sound_vault_pro(request):
    return render(request, 'soundboard/desktop.html')