from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data
        serializer = Loginserializer(data=data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user is None:
                return Response({'message': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "success": "User authenticated successfully."
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                


class IndexView(APIView):
    permission_classes = [AllowAny] 
    
    def get(self, request):
        latest_questions = Question.objects.order_by('pub_date')[-5]
        serializer = QuestionSerializer(latest_questions, many=True)
        return Response(serializer.data)


class DetailView(APIView):
    permission_classes = [AllowAny] 
    def get(request,self,pk):
        question = get_object_or_404(Question,pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)



class ResultsView(APIView):
    permission_classes = [AllowAny]
    def get(request,self,pk):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

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