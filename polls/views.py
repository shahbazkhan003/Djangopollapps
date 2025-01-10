from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from rest_framework.generics import *
from .models import Choice, Question
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny

class IndexView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Question.objects.order_by('-pub_date')[:5]
    serializer_class = QuestionSerializer

class DetailView(APIView):
    permission_classes = [IsAuthenticated] 
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ResultsView(APIView):
    permission_classes = [IsAuthenticated] 
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

class vote(APIView):
    permission_classes = [IsAuthenticated] 
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