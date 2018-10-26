from django.urls import path, include
from . import views

game_urlpatterns = ([
    path('', views.index, name = 'index'),
    path('move/<int:x>/<int:y>/', views.move, name='move'),
    path('new_game/', views.new_game, name="new_game")
], 'game')

urlpatterns = [
    path('game/', include(game_urlpatterns))
]
