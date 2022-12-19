from django.contrib import admin

from . models import Choise, Question

#crear las respuestas al mismo tiempo que creo las preguntas
class ChoiseInLine(admin.StackedInline):
  model = Choise
  extra = 3 #generar minimo 3 respuestas por defecto a cada pregunta


#cambiando el orden de los inputs para crear preguntas desde el admin
class QuestionAdmin(admin.ModelAdmin):
  fields = ["pub_date","question_text"]
  inlines = [ChoiseInLine] #se agregan todas las inline que esten creadas, en este caso solo 1
  list_display = ("question_text","pub_date","was_published_recently")  #afecta la lista de las preguntas en el Django-admin
  list_filter = ['pub_date']
  search_fields= ["question_text"]
admin.site.register(Question,QuestionAdmin)