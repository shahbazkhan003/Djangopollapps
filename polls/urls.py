from django.urls import path
from . import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "polls"
urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),      
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    path("<int:question_id>/vote/", views.vote.as_view(), name="vote"),

]