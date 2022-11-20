from jj_event_app import views_contributor
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('',views_contributor.index),
    path('read/<id>/',views_contributor.read),
    path('create/',views_contributor.create),
    path('delete/',views_contributor.delete),
    path('update/<id>/',views_contributor.update),
    path('student/',views_contributor.student_see),
    path('read_sutdent/<id>/',views_contributor.read_sutdent),

]