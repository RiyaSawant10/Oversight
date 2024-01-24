from django.db import models

class user(models.Model):
    email = models.CharField(max_length=30)
    ideas = models.TextField(blank=True)
    questions = models.TextField(blank=True)
    notes = models.TextField(blank=True)
