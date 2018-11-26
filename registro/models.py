from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Registros(models.Model):

    title = models.CharField(max_length=255, null=False)

    description = models.CharField(max_length=255, null=False)

    created_date = models.DateTimeField(
            default=timezone.now)


    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default='10')

    def __str__(self):
        return self.title

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='profile_image', blank = False)

    encode = models.TextField(max_length=2000, blank=True)

    mac_address = models.TextField(max_length=17, blank = False, default = '00:00:00:00:00:00')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# def create_profile(sender, **kwargs):
#     if kwargs['created']:
#         user_profile = Profile.objects.create(user=kwargs['instance'])

# post_save.connect(create_profile, sender=User)
