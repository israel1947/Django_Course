from django.db import models
from django.utils import timezone
from django.contrib import admin


import datetime

class Question(models.Model):
  question_text = models.CharField(max_length=200) #tipo de datos string
  pub_date = models.DateTimeField("date published")
  
  def __str__(self):
    return self.question_text
  
  #sirve para mejorar la UI del Django-admin
  @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently',
    )
  #definir que una pregunta es reciente cuando es igual o menor a la fecha actual
  def was_published_recently(self):
    return timezone.now()>= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
  
class Choise(models.Model):
  #on_delete=models.CASCADE: elimina la pregunta y todas las respuestas que esta tenga
  #Question: significa que hereda de la clase Question
  question = models.ForeignKey(Question,on_delete=models.CASCADE)
  choise_text = models.CharField(max_length=200)
  vote = models.IntegerField(default=0)
  
  def __str__(self):
    return self.choise_text