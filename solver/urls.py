from django.urls import path
from . import views

urlpatterns = [
    path('', views.PuzzleCreate.as_view(), name='index'),
    path('<uuid:uuid>/solution/', views.PuzzleSolutionView.as_view(), name='puzzle-solution'),
    path('create', views.PuzzleCreate.as_view(), name='puzzle-create'),
    path('<uuid:uuid>/enter/', views.enter_puzzle, name='puzzle-entry'),
    path('<uuid:uuid>/blank/', views.PuzzleBlankView.as_view(), name='puzzle-blank'),
]
