from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, FileExtensionValidator
from django.utils import timezone
from mutagen.mp3 import MP3
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

def mp3_validator(file):
	try:
		sound = MP3(file.open())
	except Exception as e:
		print(e)
		raise ValidationError("File is not an MP3 file")
	if sound.info.length > 30:
		raise ValidationError("Sound is too long, maximum sound length is 30 seconds.")

class Sound(models.Model):
	name = models.CharField(max_length=30)
	uploader = models.ForeignKey(User, on_delete=models.CASCADE)
	createdAt = models.DateField(default=timezone.now)
	length = models.DecimalField(validators=[MaxValueValidator(30)], decimal_places=1, max_digits=3)
	soundFile = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['mp3']),mp3_validator])
	likes = models.ManyToManyField(User, related_name="sound_post")

	def save(self, *args, **kwargs):
		length = MP3(self.soundFile.open()).info.length
		self.length = length 
		super(Sound, self).save(*args, **kwargs)

	def __str__(self):
		return self.name	
	
	
	def get_absolute_url(self):
		return reverse('sound-detail', kwargs={'pk': self.pk})