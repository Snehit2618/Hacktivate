
from django.contrib import admin
from django.urls import path
from resumes import views

urlpatterns = [
    path("admin/", admin.site.urls),
     path('interview/', views.interview_view, name='interview'),
    path('evaluate_answer/', views.evaluate_answer_view, name='evaluate_answer'),
]