from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class PlatformConfig(models.Model):
    base_url = models.URLField()
    secret_key = models.CharField(max_length=2048)


class PlatformProfile(models.Model):
    class PlatformUserType(models.TextChoices):
        UNSPECIFIED = 'unspecified'
        CLIENT = 'client'
        CAREPROVIDER = 'careprovider'

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    platform_user_id = models.CharField(max_length=255, null=True)
    platform_user_type = models.CharField(choices=PlatformUserType, default=PlatformUserType.UNSPECIFIED, max_length=32)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Platform {self.platform_user_type}: {self.pk}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        new_profile = PlatformProfile.objects.create(
            user=instance,
        )
        new_profile.save()
