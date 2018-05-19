from django.contrib import admin
from django.urls import path
from app_proyecto import views

urlpatterns = [
    path('admin/', admin.site.urls), #Administraciòn por defecto

    #LINKS DE SESIÓN
    path('', views.login, name = 'login'),
    path('login/', views.login, name = 'login'), #Iniciar sesiòn
    path('salir/', views.logout, name = 'salir'),

    #LINKS DEL GERENTE
    path('inicio_gerente/', views.inicio_gerente, name = 'inicio_gerente'),
    path('consulta_empleados/', views.consulta_empleados.as_view(), name = 'consulta_empleados'),
    path('Todos_Examenes/', views.Todos_Examenes.as_view(), name = 'Todos_Examenes'),
    path('Cantidad_Empleados_Area/', views.Cantidad_Empleados_Area.as_view(), name = 'Cantidad_Empleados_Area'),
    path('Modificar_Dictamen_Examen/', views.Modificar_Dictamen_Examen.as_view(), name = 'Modificar_Dictamen_Examen'),
    path('form_modificar_dictamen/', views.form_modificar_dictamen, name = 'form_modificar_dictamen'),

#FORMULARIO
   # 1.- Crear a la persona
	path('form_persona/', views.form_persona.as_view(), name = 'form_persona'),
	path('form_persona_domicilio/', views.form_persona_domicilio.as_view(), name = 'form_persona_domicilio'),

    #2.- Json
    path("json_supervisor/", views.json_supervisor),


    #Examenes
    path('examen_jefe_abarrotes/', views.examen_jefe_abarrotes, name = 'examen_jefe_abarrotes'),
    path('examen_cajas/', views.examen_cajas, name = 'examen_cajas'),

     #LINKS DEL SUPERVISOR
    path('inicio_supervisor/', views.inicio_supervisor, name = 'inicio_supervisor'),
    path('sup_consulta_empleados/', views.sup_consulta_empleados.as_view(), name = 'sup_consulta_empleados'),
    path('sup_Todos_Examenes/', views.sup_Todos_Examenes.as_view(), name = 'sup_Todos_Examenes'),
    path('sup_Cantidad_Empleados_Area/', views.sup_Cantidad_Empleados_Area.as_view(), name = 'sup_Cantidad_Empleados_Area'),
]
