from django.urls import path
from . import views

urlpatterns = [
    
    path('logint/', views.login_view, name='logint'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    # URLs para usuarios
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:usuario_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # URLs para eventos
    path('eventos/', views.listar_eventos, name='listar_eventos'),
    path('eventos/crear/', views.crear_evento, name='crear_evento'),
    path('eventos/editar/<int:evento_id>/', views.editar_evento, name='editar_evento'),
    path('eventos/eliminar/<int:evento_id>/', views.eliminar_evento, name='eliminar_evento'),

    # URL para inscribir usuarios manualmente
    path('inscripciones/inscribir/', views.inscribir_usuario, name='inscribir_usuario'),
    path('buscar_eventos_usuario/<int:usuario_id>/', views.buscar_eventos_usuario, name='buscar_eventos_usuario'),
    path('desinscribir/<int:evento_id>/<int:usuario_id>/', views.desinscribir_usuario, name='desinscribir_usuario'),
    
    path('exportar-usuarios/', views.exportar_usuarios, name='exportar_usuarios'),
]
