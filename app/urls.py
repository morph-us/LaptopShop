from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('view/', views.view, name='index'),
    path('search/', views.search, name='index'),
    path('insert/', views.insertdata, name='index'),
    path('update/', views.update, name='index'),
    path('removemodel/', views.removemodel, name='index'),
    
    path('outofstock/', views.outofstock, name='index'),
    path('insertform/', views.insertform, name='index'),
    path('updateform/', views.updateform, name='index'),
    path('removemodelform/', views.removemodelform, name='index'),
    
    
    path('csvfile/', views.csvfile, name='index'),
    path('searchcsvfile/', views.searchcsvfile, name='index'),
]
