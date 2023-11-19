from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPreference(models.Model):
    user = models.OneToOneField(to = User, on_delete = models.CASCADE)
    currency = models.CharField(max_length = 255, verbose_name = "Currency", blank = True, null = True)
    
    def __str__(self) -> str:
        return f"{str(self.user)}s preferences"
    
    class Meta:
        verbose_name_plural = "User Preferences"