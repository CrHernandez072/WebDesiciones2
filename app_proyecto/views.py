# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic.list import ListView

from django.http import HttpResponse
from django.core import serializers
import json

import datetime

#Se instancia para contar los elementos que agrupo en la vista (Cantidad_Empleados_Area)
from django.db.models import Count

from app_proyecto import models
# Create your views here.

def login(request):

	#SE EJECUTARÁ ESTA ACCION SI SE ACCEDE A LA PAGINA DEL MODO POST
	if request.method == "POST":
		
		# 1. Verifica si el curp ingresado existe en la bd
		if models.Personas.objects.filter(Curp = request.POST.get('f_curp')).exists():

			datos = models.Empleado.objects.get(Curp=request.POST.get('f_curp'))
			if datos.contraseña == request.POST.get('f_contraseña'):

				#SE CREAN VARIABLES DE SESION
				request.session['curp'] = str(datos.Curp)
				request.session['id_puesto'] = str(datos.Id_Puesto)
		
				if str(datos.Id_Puesto == "Supervisor"):
					return redirect('inicio_supervisor')
				elif str(datos.Id_Puesto == "Gerente"):
					return redirect('inicio_gerente')

			else:
				return render(request, 'app_proyecto/login.html', {"error": "Usuario y/o contraseña incorrecta", "css": "border: 1px; box-shadow: 2px 5px 15px #888888; border-radius: 5px;"})
		else:
			return render(request, 'app_proyecto/login.html', {"error": "Usuario y/o contraseña incorrecta", "css": "border: 1px; box-shadow: 2px 5px 15px #888888; border-radius: 5px;"})
	
	#EL USUARIO TIPEÓ LA URL
	else:
		return render(request, 'app_proyecto/login.html')


def logout(request):
    #SE DESTRUYEN LAS VARIABLES DE SESION
    try:
        del request.session['curp']
        del request.session['id_puesto']
    except KeyError:
        pass
	#DESPUES DE DESTRUIR LAS VARIABLES DE SESIÓN, TE REDIGIRÁ A LA URL QUE TENGA EL NOMBRE "login"
    return redirect('login')


# ENLACES DEL GERENTE!
def inicio_gerente(request):
	return render(request, 'app_proyecto/gerente/index.html')

class Todos_Examenes(ListView):
    template_name= "app_proyecto/gerente/Todos_Examenes.html"
    queryset = models.ResultadoExamenes.objects.select_related()

class Cantidad_Empleados_Area(ListView):
    template_name= "app_proyecto/gerente/Cantidad_Empleados_Area.html"
    queryset = models.Empleado.objects.values('Id_Puesto').annotate(cantidad=Count('Id_Puesto'))

class consulta_empleados(ListView):
    template_name= "app_proyecto/gerente/consulta_empleados.html"
    queryset = models.Empleado.objects.all()

from django.db.models import Q

class Modificar_Dictamen_Examen(ListView):
    template_name= "app_proyecto/gerente/Modificar_Dictamen_Examen.html"
    queryset = models.ResultadoExamenes.objects.filter(Dictamen = "Rechazado")

    def get_context_data(self,**kwargs):
    	pass
    	context = super().get_context_data(**kwargs)
    	context['Ids_Puestos'] = models.PuestoEmpleado.objects.all().filter(~Q(Id_Puesto = "Gerente"), ~Q(Id_Puesto = "Supervisor"))
    	return context

def form_modificar_dictamen(request):
	#SE EJECUTARÁ ESTA ACCION SI SE ACCEDE A LA PAGINA DEL MODO POST
	if request.method == "POST" and str(request.POST.get('Puesto')) != "":
		numero = str(request.POST.get('Num_Examen'))
		curp = str(request.POST.get('Curp'))
		id_puesto = str(request.POST.get('Puesto'))
		examen = str(request.POST.get('Examen'))


		re = models.ResultadoExamenes.objects.get(Num_Examen=models.ExamenPersonas.objects.get(Num_Examen=int(numero)))
		re.Puntaje = 0000
		re.Dictamen = "Aceptado"
		re.save()

		em = models.Empleado(Curp=models.Personas.objects.get(Curp=curp), Id_Puesto=models.PuestoEmpleado.objects.get(Id_Puesto=id_puesto))
		em.save()

		return redirect('Modificar_Dictamen_Examen')
	else:
		supervisor = models.Empleado.objects.get(Id_Puesto = "Supervisor")
		contexto = {"CONTEXTO": supervisor.No_Empleado, "Contraseña": supervisor.contraseña}
		return redirect('Modificar_Dictamen_Examen')

#FORMULARIOS OBLIGATORIOS
class form_persona(CreateView):
    template_name= "app_proyecto/form_persona.html"
    model = models.Personas
    fields = "__all__"
    success_url = reverse_lazy("login")

class form_persona_domicilio(CreateView):
    template_name= "app_proyecto/form_persona_domicilio.html"
    model = models.DireccionPersonas
    fields = "__all__"
    success_url = reverse_lazy("login")

def json_supervisor(request):
	data = serializers.serialize('json', models.Empleado.objects.filter(Id_Puesto = 2))
	return HttpResponse(data, "application/json")


#----------------- EXAMENES -----------------
def examen_jefe_abarrotes(request):	
	#SE EJECUTARÁ ESTA ACCION SI SE ACCEDE A LA PAGINA DEL MODO POST
	if request.method == "POST":
		curp = str(request.POST.get('curp'))
		
		# 1. Verifica si el curp ingresado existe en la bd
		if models.Personas.objects.filter(Curp = curp).exists():
			detalle_examen = models.Examen.objects.get(Id_Examen="Examen Jefe Abarrotes") #Obtiene los detalles del examen

			id_examen = detalle_examen.Id_Examen
			minimo = int(detalle_examen.puntaje_minimo)
			maximo = int(detalle_examen.puntaje_maximo)

			#Cacha los valores que trae el formulario
			puntaje_edad = int(request.POST.get('edad'))
			puntaje_ingles = int(request.POST.get('ingles'))
			puntaje_estudios = int(request.POST.get('estudios'))		
			arr_consultas = request.POST.getlist('consultas') #Lista de valores seleccionados
			arr_experiencia = request.POST.getlist('experiencia') #Lista de valores seleccionados
			arr_conocimientos = request.POST.getlist('conocimientos') #Lista de valores seleccionados

			puntale_consulta = 0
			puntale_experiencia = 0
			puntale_conocimiento = 0

			for puntaje in arr_consultas:
				puntale_consulta = puntale_consulta + int(puntaje)

			for puntaje in arr_experiencia:
				puntale_experiencia = puntale_experiencia + int(puntaje)

			for puntaje in arr_conocimientos:
				puntale_conocimiento = puntale_conocimiento + int(puntaje)
			
			resultado_examen = puntaje_edad + puntaje_ingles + puntaje_estudios + puntale_consulta + puntale_experiencia + puntale_conocimiento

			#1. Guardando el examenrealizado 
			p = models.ExamenPersonas(Curp=models.Personas.objects.get(Curp=curp), Id_Examen=models.Examen.objects.get(Id_Examen=id_examen))
			p.save()

			#2. Extraer "num_examen"
			detalle = models.ExamenPersonas.objects.get(Curp=curp, Id_Examen="Examen Jefe Abarrotes")
			num_examen = detalle.Num_Examen

			if resultado_examen >= minimo:
				p = models.ResultadoExamenes(Num_Examen=models.ExamenPersonas.objects.get(Num_Examen=num_examen), Puntaje=resultado_examen, Dictamen = "Aceptado")
				p.save()

				e = models.Empleado(Curp=models.Personas.objects.get(Curp=curp), Id_Puesto=models.PuestoEmpleado.objects.get(Id_Puesto="Jefe de abarrotes"))
				e.save()

				return render(request, "app_proyecto/examenes/examen_jefe_abarrotes.html", {"Mensaje": "Tu examen ha sido guardado", "css": "border: 1px; box-shadow: 2px 5px 15px #888888; border-radius: 5px;"})
			else:
				p = models.ResultadoExamenes(Num_Examen=models.ExamenPersonas.objects.get(Num_Examen=num_examen), Puntaje=resultado_examen, Dictamen = "Rechazado")
				p.save()
				return render(request, "app_proyecto/examenes/examen_jefe_abarrotes.html", {"Mensaje": "Tu examen ha sido guardado", "css": "border: 1px; box-shadow: 2px 5px 15px #888888; border-radius: 5px;"})
		else:
			supervisor = models.Empleado.objects.get(Id_Puesto = "Supervisor")
			contexto = {'resultado':"El Curp ingresado es erroneo", "r_color": "red"}
			return render(request, "app_proyecto/examenes/examen_cajas.html", contexto)
	else:
		supervisor = models.Empleado.objects.get(Id_Puesto = "Supervisor")
		contexto = {"No_Empleado": supervisor.No_Empleado, "Contraseña": supervisor.contraseña}
		return render(request, "app_proyecto/examenes/examen_jefe_abarrotes.html", contexto)

def examen_cajas(request):	
	#SE EJECUTARÁ ESTA ACCION SI SE ACCEDE A LA PAGINA DEL MODO POST
	if request.method == "POST":
		curp = str(request.POST.get('curp'))

		# 1. Verifica si el curp ingresado existe en la bd
		if models.Personas.objects.filter(Curp = curp).exists():
			detalle_examen = models.Examen.objects.get(Id_Examen="Examen Jefe de Cajas") #Obtiene los detalles del examen

			id_examen = detalle_examen.Id_Examen
			minimo = int(detalle_examen.puntaje_minimo)
			maximo = int(detalle_examen.puntaje_maximo)

			#Cacha los valores que trae el formulario
			puntaje_edad = int(request.POST.get('edad'))
			puntaje_ingles = int(request.POST.get('ingles'))
			puntaje_estudios = int(request.POST.get('estudios'))		
			arr_consultas = request.POST.getlist('consultas') #Lista de valores seleccionados
			arr_experiencia = request.POST.getlist('experiencia') #Lista de valores seleccionados

			puntale_consulta = 0
			puntale_experiencia = 0

			for puntaje in arr_consultas:
				puntale_consulta = puntale_consulta + int(puntaje)

			for puntaje in arr_experiencia:
				puntale_experiencia = puntale_experiencia + int(puntaje)

		
			resultado_examen = puntaje_edad + puntaje_ingles + puntaje_estudios + puntale_consulta + puntale_experiencia

			#1. Guardando el examenrealizado 
			p = models.ExamenPersonas(Curp=models.Personas.objects.get(Curp=curp), Id_Examen=models.Examen.objects.get(Id_Examen=id_examen))
			p.save()

			#2. Extraer "num_examen"
			detalle = models.ExamenPersonas.objects.get(Curp=curp, Id_Examen="Examen Jefe de Cajas")
			num_examen = detalle.Num_Examen

			if resultado_examen >= minimo:
				p = models.ResultadoExamenes(Num_Examen=models.ExamenPersonas.objects.get(Num_Examen=num_examen), Puntaje=resultado_examen, Dictamen = "Aceptado")
				p.save()

				e = models.Empleado(Curp=models.Personas.objects.get(Curp=curp), Id_Puesto=models.PuestoEmpleado.objects.get(Id_Puesto="Jefe de Cajas"))
				e.save()

				contexto = {'resultado':"Aceptado", "r_color": "green"}
				return render(request, "app_proyecto/login.html", contexto)
			else:
				p = models.ResultadoExamenes(Num_Examen=models.ExamenPersonas.objects.get(Num_Examen=num_examen), Puntaje=resultado_examen, Dictamen = "Rechazado")
				p.save()
				contexto = {'resultado':"Suerte para la próxima bro :V", "r_color": "red"}
				return render(request, "app_proyecto/examenes/examen_cajas.html", contexto)		
		else:
			supervisor = models.Empleado.objects.get(Id_Puesto = "Supervisor")
			contexto = {'resultado':"El Curp ingresado es erroneo", "r_color": "red"}
			return render(request, "app_proyecto/examenes/examen_cajas.html", contexto)
	else:
		supervisor = models.Empleado.objects.get(Id_Puesto = "Supervisor")
		contexto = {"No_Empleado": supervisor.No_Empleado, "Contraseña": supervisor.contraseña}
		return render(request, "app_proyecto/examenes/examen_cajas.html", contexto)

# ENLACES DEL SUPERVISOR!
def inicio_supervisor(request):
	return render(request, 'app_proyecto/supervisor/index.html')

class sup_Todos_Examenes(ListView):
    template_name= "app_proyecto/supervisor/Todos_Examenes.html"
    queryset = models.ResultadoExamenes.objects.select_related()

class sup_Cantidad_Empleados_Area(ListView):
    template_name= "app_proyecto/supervisor/Cantidad_Empleados_Area.html"
    queryset = models.Empleado.objects.values('Id_Puesto').annotate(cantidad=Count('Id_Puesto'))

class sup_consulta_empleados(ListView):
    template_name= "app_proyecto/supervisor/consulta_empleados.html"
    queryset = models.Empleado.objects.all()

from django.views.generic import View
from django_proyecto import utils


class gr_todos_examenes(View):
	#Regresa el pdf
	def get(self, request, *args, **kwagrs):
		fecha = datetime.datetime.now()
		resultados = models.ResultadoExamenes.objects.select_related()
		pdf = utils.render_pdf("app_proyecto/reportes/gr_todos_examenes.html", {"object_list": resultados, "fecha": fecha})

		return HttpResponse(pdf, content_type="application/pdf")

class gr_cantidad_empleado_area(View):
	#Regresa el pdf
	def get(self, request, *args, **kwagrs):
		fecha = datetime.datetime.now()
		resultados = models.Empleado.objects.values('Id_Puesto').annotate(cantidad=Count('Id_Puesto'))
		pdf = utils.render_pdf("app_proyecto/reportes/gr_cantidad_empleado_area.html", {"object_list": resultados, "fecha": fecha})

		return HttpResponse(pdf, content_type="application/pdf")

class gr_consulta_empleados(View):
	#Regresa el pdf
	def get(self, request, *args, **kwagrs):
		fecha = datetime.datetime.now()
		resultados = models.Empleado.objects.all()
		pdf = utils.render_pdf("app_proyecto/reportes/gr_consulta_empleados.html", {"object_list": resultados, "fecha": fecha})

		return HttpResponse(pdf, content_type="application/pdf")