from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import QuestionSerializer



class IndexView(APIView):
    def get(self, request):
        latest_questions = Question.objects.order_by('pub_date')[-5]
        serializer = QuestionSerializer(latest_questions, many=True)
        return Response(serializer.data)


class DetailView(APIView):
    def get(request,self,pk):
        question = get_object_or_404(Question,pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)



class ResultsView(APIView):
    def get(request,self,pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

class vote(APIView):
    def post(self, request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        try:
            selected_choice = question.choice_set.get(pk=request.data["choice"])
        except (KeyError, Choice.DoesNotExist):
            return Response({"error": "You didn't select a choice."}, status=400)
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
            serializer = QuestionSerializer(question)
            return Response(serializer.data)