
from django.urls import path
from . import views

app_name = 'feed'


urlpatterns = [
    path('', views.feedMain, name='feedMain'),
    path('video/<int:id>/', views.seeVideo, name='seeVideo'),
    path('upload/', views.uploadVideo, name='uploadVideo'),
    path('edit/<int:id>', views.editVideo, name='editVideo'),
    path('delet/<int:id>', views.deletVideo, name='deletVideo'),
    path('videosonsearch/', views.videosOnSearch, name='videosOnSearch'),
]

