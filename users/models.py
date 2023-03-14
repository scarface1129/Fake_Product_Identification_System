from django.db import models
from django.contrib.auth.models import AbstractUser
from .utils import code_generator
from django.urls import reverse
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.conf import settings
from company.models import Company
from django.conf import settings


User = settings.AUTH_USER_MODEL
class User(AbstractUser):
    # my_custom_field = models.CharField(max_length=2)
    activation_key     = models.CharField(max_length=120, blank=True, null=True)
    activated          = models.BooleanField(default=False)

# Create your models here.
def send_activation_email(self):
        pass
        if self.activated:
            pass
        else:
            self.activation_key = code_generator()#'somekey'
            print(self.activation_key)
            self.save()
            #path_=reverse()
            path_ = reverse("activate", kwargs={"code":self.activation_key})
            subject = 'Activate Account'
            from_email = 'agboemmanuel002@gmail.com'
            message = f'Activate your account here: {path_}'
            recipient_list = [self.email]
            html_message = f'Activate your account here: {path_}'
            sent_mail= send_mail(
                    subject,
                    from_email,
                    message,
                    recipient_list,
                    fail_silently=False,
                    html_message=html_message)
            
            return sent_mail
def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        profile, is_created = User.objects.get_or_create(user=instance)
        


post_save.connect(post_save_user_receiver, sender=Company)