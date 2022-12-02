from django.db import models

class Question(models.Model):
  question_text = models.CharField(max_length=200) #tipo de datos string
  pub_date = models.DateTimeField("date published")
  
class Choise(models.Model):
  #on_delete=models.CASCADE: elimina la pregunta y todas las respuestas que esta tenga
  #Question: significa que hereda de la clase Question
  question = models.ForeignKey(Question,on_delete=models.CASCADE)
  choise_text = models.CharField(max_length=200)
  vote = models.IntegerField(default=0)