from django.db import models
from django.utils import timezone

class Registros(models.Model):

    title = models.CharField(max_length=255, null=False)

    description = models.CharField(max_length=255, null=False)

    created_date = models.DateTimeField(
            default=timezone.now)

    
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, default='10')

    def __str__(self):
        return self.title