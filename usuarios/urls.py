from django.urls import path
from .views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', logout_view, name='logout'), 
    path('home/', home, name='home'),
    path('crear-evento/', create_evento, name='create_evento'),
    path('ver-eventos/', ver_eventos, name='ver_eventos'),
    path('mis-eventos/', mis_eventos, name='mis_eventos'),
    path('modificar-evento/<int:evento_id>/', modificar_evento, name='modificar_evento'),
    path('inscribirme-evento/<int:evento_id>/', inscribirme_evento, name='inscribirme_evento'),
    path('eliminar-evento/<int:evento_id>/', eliminar_evento, name='eliminar_evento'),
    path('desinscribirme-evento/<int:evento_id>/', desinscribirme_evento, name='desinscribirme_evento'),
]