from django.db import models
from base.models import User, Debtor

class Notifications(models.Model):
    user = models.ForeignKey("base.User", on_delete=models.CASCADE)
    partial_id = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=255)
    is_read = models.CharField(max_length=50, blank=True, default = 'no')
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title
    
