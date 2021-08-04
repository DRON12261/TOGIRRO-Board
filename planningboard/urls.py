from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name=''),
    path('login', views.auth, name='login'),
    path('board', views.board, name='board'),
    path('adminlobby', views.adminlobby, name='adminlobby'),
    path('messenger', views.messenger, name="messenger")
]