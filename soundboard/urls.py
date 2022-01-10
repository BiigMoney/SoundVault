from django.urls import path 
from .views import SoundListView, SoundDetailView, SoundCreateView, SoundDeleteView, LikeView, sound_vault_pro
from . import views

urlpatterns = [
	path("", SoundListView.as_view(), name="home"),
	path("soundvaultpro/", sound_vault_pro, name="sound-vault-pro"),
	path('sound/<int:pk>/', SoundDetailView.as_view(), name='sound-detail'),
	path('sound/<int:pk>/delete', SoundDeleteView.as_view(), name='sound-delete'),
	path('sound/new/', SoundCreateView.as_view(), name='sound-create'),
	path('like/<int:pk>', LikeView.as_view(), name='like-sound')
]