import datetime


from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from . models import Question


class QuestionModelTest(TestCase):
  
  def setUp(self):
    self.question = Question(question_text="¿La mejor consola de videojuegos 2022?")
  
  def testWasPublishedRecentlyWithFutureQuestion(self):
    """ Retorna false cuando la pregunta tiene una fecha de publicacion a futuro """
    time= timezone.now() + datetime.timedelta(days=30)
    self.question.pub_date= time
    self.assertIs(self.question.was_published_recently(), False)
    
  def testWasPublishedWithPresentQuestion(self):
    """ Retorna TRUE cuando la pregunta tiene una fecha de publicacion en fecha presente """
    time= timezone.now() + datetime.timedelta(hours=-23)
    self.question.pub_date= time
    self.assertIs(self.question.was_published_recently(), True)
    

def pba(que,tim):
   time= timezone.now() + datetime.timedelta(days=tim)  
   question = Question.objects.create(question_text=que, pub_date=time)
   return question
class QuestionIndexViewTest(TestCase):
  
  def testNotQuestion(self):
    """ SI NO HAY PREGUNTA EXISTENTE SE PUBLICA UN MSG """
    response = self.client.get(reverse("poll:index"))
    self.assertEqual(response.status_code,200)
    self.assertContains(response,"No existe encuesta!.")
    self.assertQuerysetEqual(response.context["latest_question_list"], [] )
  
  def testFutureQuestion(self):
    """ NO MOSTRAR LAS PREGUNTAS QUE NO CORRESPONDAN A LA FECHA ACTUAL """
    response = self.client.get(reverse("poll:index"))
    time= timezone.now() + datetime.timedelta(days=30)
    pba = Question(question_text="¿el mejor teléfono en el 2025?", pub_date=time)
    
    self.assertNotIn(pba,response.context["latest_question_list"])
  
  def testPassQuestion(self):
    """ MOSTRAR PREGUNTAS ESCRITAS EN EL PASADO """
    time= timezone.now() + datetime.timedelta(days=-10)
    pba = Question.objects.create(question_text="la mejor marca de cualquier cosa?", pub_date=time)
    response = self.client.get(reverse("poll:index"))
    
    self.assertQuerysetEqual(response.context["latest_question_list"],[pba])
    
  
  def testFutureQuestionAndPassQuestion(self):
   """ MOSTAR SOLO PREGUNTAS DEL PASADO EN EL INDEX VIEWS """
   questionPass= pba("la mejor marca de cualquier cosa nuevamente 1?",-30)
   futureQuestion = pba("la mejor marca de cualquier cosa nuevamente 2?",30)
  
   response = self.client.get(reverse("poll:index"))
   self.assertQuerysetEqual(response.context["latest_question_list"],[questionPass])
  
  
  def testTwoPastQuestion(self):
   """ MULTIPLES PREGUNTAS DEL PASADO EN LA PAGINA DE PREGUNTA """
   questionPass1= pba("la mejor marca de cualquier cosa otra vez 1?",-30)
   questionPass2 = pba("la mejor marca de cualquier cosa otra vez 2?",-40)
  
   response= self.client.get(reverse("poll:index"))
   self.assertQuerysetEqual(response.context["latest_question_list"],[questionPass1,questionPass2])
   
  def testTwoFutureQuestion(self):
    """ MULTIPLES PREGUNTAS DEL FUTURO EN LA PAGINA DE PREGUNTA """
    response = self.client.get(reverse("poll:index"))
    questionFuture1= pba("la mejor marca de cualquier cosa otra vez 1?",30)
    questionFuture2= pba("la mejor marca de cualquier cosa otra vez 2?",30)
    
    self.assertQuerysetEqual(response.context["latest_question_list"],[])

class QuestionDetailViewTest(TestCase):
  
  def futureQuestion1(self):
    """ NO MOSTRAR LA PREGUNTA CUANDO UN USUARIO CONOCE LA URL  """
    futureQuestion = pba("esta es la pagina de detalle?",30)
    url= reverse("poll:detail",args=(futureQuestion.pk,))
    response = self.client.get(url)
    self.assertEqual(response.status_code,404)
  
  def pastQuestion1(self):
    """ MOSTRAR LA PREGUNTA CUANDO ESTA SEA DEL PASADO """
    pastQuestion = pba("esta es la pagina de detalle?",-30)
    url= reverse("poll:detail",args=(pastQuestion.pk,))
    response = self.client.get(url)
    self.assertContains(response,pastQuestion.question_text)
    
