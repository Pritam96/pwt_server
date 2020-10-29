from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('home_xls', views.home_xls, name='home_xls'),
    path('summary/summary_1', views.summary_1, name='summary_1'),
    path('summary/pipeshiftduration_summary_1', views.pipeshiftduration_summary_1, name='pipeshiftduration_summary_1'),
    path('summary/summary_2', views.summary_2, name='summary_2'),
    path('summary/summary_4', views.summary_4, name='summary_4'),
    path('summary/material_issue_summary_4', views.material_issue_summary_4, name='material_issue_summary_4'),
    path('summary/summary_7', views.summary_7, name='summary_7'),
    path('summary/summary_8', views.summary_8, name='summary_8'),
    path('summary/summary_format', views.summary_format, name='summary_format'),
    path('summary', views.summary, name='summary'),
    path('logout', views.log_out, name='log_out')
]