from django.db import models

# Create your models here.

# add last created token at and user registered at in the model and views

class UserData(models.Model):
    email = models.EmailField(verbose_name = "Email")
    email_verification_token = models.TextField(blank=True, null=True, verbose_name="Verification Token")
    created_at = models.DateTimeField(auto_now=True, verbose_name="Created at")

    class Meta:
        verbose_name = "User Data"
        verbose_name_plural = "User Data"