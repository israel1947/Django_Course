from django.shortcuts import  get_object_or_404, render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from django.utils import timezone

from .models import Choise, Question


#HOME VIEW
""" def index(request):
  latest_question_list = Question.objects.all()
  context = {
    "latest_question_list": latest_question_list
    }
  return render(request,"poll/index.html",context) """
class IndexView(generic.ListView):
  """ traer a la vista las publicaciones más recientes """
  template_name = "poll/index.html"
  context_object_name ="latest_question_list"
  
  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
  
#DETAIL VIEW
""" def detail(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  questionDiccionario = {
    "question":question
  }
  return render(request, "poll/detail.html",questionDiccionario) """
class DetailView(generic.DetailView):
  model = Question
  template_name ="poll/detail.html"
  
  def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now())

#RESULT VIEW
""" def result(request, question_id):
  question = get_object_or_404(Question,pk=question_id)
  resultDiccionario={
    "question":question
  }
  return render(request, "poll/result.html",resultDiccionario) """
class ResultView(generic.DetailView):
  model = Question
  template_name ="poll/result.html"

# VOTE VIEW
def vote(request, question_id):
  question = get_object_or_404(Question, pk= question_id)
  errorDiccionario={
    "question":question,
    "errorMessage":"No elegiste una respuesta.!"
  }
  
  try:
    #pk=request.POST["choise"]: hace referencia al name que se definio en el form HTML
    #es decir, se optiene a seleccion que hizo el usuario
    selecter_choise = question.choise_set.get(pk=request.POST["choise"])

  except(KeyError,Choise.DoesNotExist):
    return render(request, "poll/detail.html",errorDiccionario)
  
  else:
    #se suma un voto a dicha pregunta
    selecter_choise.vote += 1
    #se guarda el voto en la DB
    selecter_choise.save()
    #despues de votar redirige al usuario a la pagina de resutados
    return HttpResponseRedirect(reverse("poll:result", args=(question.id,)))