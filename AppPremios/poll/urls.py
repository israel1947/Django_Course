from django.urls import path
from . import views

app_name="poll"

urlpatterns = [
  #localhost:8000/poll/
  path("",views.IndexView.as_view(), name="index"),
  #localhost:8000/poll/5
  path("<int:pk>/details",views.DetailView.as_view(), name="detail"),
  #localhost:8000/poll/5/result
  path("<int:pk>/result",views.ResultView.as_view(), name="result"),
  #localhost:8000/poll/5/vote
  path("<int:question_id>/vote",views.vote, name="vote")
]