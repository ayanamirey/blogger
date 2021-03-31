from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(default=None, blank=True, null=True,
                               upload_to='users_photos/')

    def __str__(self):
        return self.user.username

    def get_username(self):
        return reverse('user-details', args=[str(self.user.username)])

    def snippet(self):
        return self.bio[:25] + '...'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class SocialNetwork(models.Model):
    title = models.CharField(max_length=63)
    class_name = models.CharField(max_length=31)
    link_to_sn = models.CharField(max_length=63)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class ConnectToSocialAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_network = models.ForeignKey(SocialNetwork, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.username} [{self.social_network}]'
