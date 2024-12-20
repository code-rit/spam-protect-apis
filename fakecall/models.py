from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.phone_number

class SpamMark(models.Model):
    marked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="marked_spam")
    reason = models.TextField(blank=True, null=True)

class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    spam_mark = models.ForeignKey(SpamMark, on_delete=models.CASCADE, related_name="spam_marks")
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.phone_number}"




