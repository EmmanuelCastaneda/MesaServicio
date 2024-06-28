from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.db import Error, transaction
from .models import *
from datetime import datetime

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
import threading
from smtplib import SMTPException
from django.http import JsonResponse


def inicio(request):
    return render(request,"login.html")


def inicioAdministrador(request):
    if request.user.is_authenticated:
        datosSesion = {"user": request.user,
                       "rol": request.user.groups.get().name}
        return render(request, "administrador/inicio.html", datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "login.html", {"mensaje": mensaje})

    
def inicioTecnico(request):
    if request.user.is_authenticated:
        datos={"user":request.user,
               "rol":request.user.groups.get().name}
        return render(request,"tecnico/inicio.html",datos)
    else: 
        mensaje="Debe iniciar sesion"
        return render(request,"login.html",{"mensaje":mensaje})

def inicioEmpleado(request):
    if request.user.is_authenticated:
        datos={"user":request.user,
               "rol":request.user.groups.get().name}
        return render(request,"empleado/inicio.html",datos)
    else: 
        mensaje="Debe iniciar sesion"
        return render(request,"login.html",{"mensaje":mensaje})

@csrf_exempt
def login(request):
    username=request.POST["correo"]
    print(username)
    password=request.POST["contraseña"]
    print(password)
    user=authenticate(username=username,password=password)
    print(user)
    if user is not None:
        # Registrar Variable de Sesion
        auth.login(request,user)
        if user.groups.filter(name='Administrativo').exists():
            return redirect('/inicioAdministrador')
        elif user.groups.filter(name='Tecnico').exists():
            return redirect('/inicioTecnico')
        else:
            return redirect('/inicioEmpleado')
    else:
        mensaje="Usuario o Contraseña Incorrecta"
        return render(request,"login.html",{"mensaje":mensaje})


# def vistaSolicitud(request):
#     if request.user.is_authenticated:
#         oficinaAmbientes= OficinaAmbiente.objects.all()
#         datosSesion={
#             "user":request.user,
#             "rol":request.user.groups.get().name,
#             "oficinaAmbientes":oficinaAmbientes
#         }
#         return render(request,'empleado/registrarSolicitud.html',datosSesion)
#     else:
#         mensaje="Inicie Sesion"
#         return render(request,"login.html",{"mensaje":mensaje})
def vistaSolicitud(request):
    if request.user.is_authenticated:
        # consultar las oficinas y ambientes registrados
        oficinaAmbientes = OficinaAmbiente.objects.all()
        datosSesion = {"user": request.user,
                       "rol": request.user.groups.get().name,
                       'oficinasAmbientes': oficinaAmbientes}
        return render(request, 'empleado/registrarSolicitud.html', datosSesion)
    else:
        mensaje = "Debe iniciar sesión"
        return render(request, "login.html", {"mensaje": mensaje})

def registrarSolicitud(request):
    try:
        with transaction.atomic():
            user = request.user
            descripcion = request.POST['txtDescripcion']
            idOficinaAmbiente = int(request.POST['cbOficinaAmbiente'])
            oficinaAmbiente = OficinaAmbiente.objects.get(pk=idOficinaAmbiente)
            solicitud = Solicitud(solUsuario=user, solDescripcion=descripcion,
                                  solOficinaAmbiente=oficinaAmbiente)
            solicitud.save()
 
            fecha = datetime.now()
            year = fecha.year

            consecutivoCaso = Solicitud.objects.filter(
                fechaHoraCreacion__year=year).count()
            consecutivoCaso = str(consecutivoCaso).rjust(5, '0')
            codigoCaso = f"REQ-{year}-{consecutivoCaso}"
            userCaso = User.objects.filter(
                groups__name__in=['Administrador']).first()
            caso = Caso(casSolicitud=solicitud,
                        casCodigo=codigoCaso, casUsuario=userCaso)
            caso.save()
            asunto = 'Registro Solicitud - Mesa de Servicio'
            mensajeCorreo = f'Cordial saludo, <b>{user.first_name} {user.last_name}</b>, nos permitimos \
                informarle que su solicitud fue registrada en nuestro sistema con el número de caso \
                <b>{codigoCaso}</b>. <br><br> Su caso será gestionado en el menor tiempo posible, \
                según los acuerdos de solución establecidos para la Mesa de Servicios del CTPI-CAUCA.\
                <br><br>Lo invitamos a ingresar a nuestro sistema en la siguiente url:\
                http://mesadeservicioctpicauca.sena.edu.co.'
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [user.email]))
            thread.start()
            mensaje = "Se ha registrado su solicitud de manera exitosa"
    except Error as error:
        transaction.rollback()
        mensaje = f"{error}"

    oficinaAmbientes = OficinaAmbiente.objects.all()
    retorno = {"mensaje": mensaje, "oficinasAmbientes": oficinaAmbientes}
    return render(request, "empleado/registrarSolicitud.html", retorno)
    
# def registrarSolicitud(request):
#     try:
#         with transaction.atomic():
#             user= request.user
#             descripcion=request.POST["descripcion"]
#             idOficinaAmbiente=int(request.POST["OficinaAmbiente"])
#             idOficinaAmbiente=idOficinaAmbiente.objects.get(pk=idOficinaAmbiente)
#             solicitud=Solicitud(solUsuario=user,
#                         solDescripcion=descripcion,
#                         solOficinaAmbiente=OficinaAmbiente)
#             solicitud.save()
#             fecha=datetime.now()
#             year =fecha.year
#             consecutivoCaso=Solicitud.object.filter(fechaHoraCreacion__year=year).count()
#             consecutivoCaso = str(consecutivoCaso).rjust(5,"0")
#             codigoCaso=f"REQ-{year}-{consecutivoCaso}"
#             userCaso=User.objects.filter(groups__name__in=['Administrador']).first()
#             caso=Caso(casSolicitud=solicitud,casCodigo=codigoCaso,casUsuario=userCaso)
#             caso.save()
#             mensaje ="Se ha registrado su solicitud de manera exitosa"
#     except Error as error:
#         transaction.rollback()
#         mensaje=f"{error}"
    
    
def enviarCorreo(asunto=None, mensaje=None, destinatario=None, archivo=None):
    remitente = settings.EMAIL_HOST_USER
    template = get_template('enviarCorreo.html')
    contenido = template.render({
        'mensaje': mensaje,
    })
    try:
        correo = EmailMultiAlternatives(
            asunto, mensaje, remitente, destinatario)
        correo.attach_alternative(contenido, 'text/html')
        if archivo != None:
            correo.attach_file(archivo)
        correo.send(fail_silently=True)
    except SMTPException as error:
        print(error)

        
def listarCasos(request):
        try:
            mensaje = ""
            listaCasos = Caso.objects.all()
            tecnicos=User.objects.filter(groups__name__in=['tecnico'])
            
        except Error as error:
            mensaje=str(error)
        retorno={'listaCasos':listaCasos,'tecnicos':tecnicos,'mensaje':mensaje}
        return render(request,'administrador/listarCasos.html',retorno)
    
def listarEmpleadosTecnicos(request):
    try:
        tecnicos=User.objects.filter(groups__name__in=['Tecnico'])
        mensaje=''
    except Error as error:
        mensaje=str(error)
    retorno={'tecnicos':tecnicos,'mensaje':mensaje}
    return JsonResponse(retorno)
                
           

    
def asignarTecnicoCaso(request):
    if request.user.is_authenticated:
        try:
            idTecnico = int(request.POST['cbTecnico'])
            userTecnico = User.objects.get(pk=idTecnico)
            idCaso = int(request.POST['idCaso'])
            caso = Caso.objects.get(pk=idCaso)
            caso.casUsuario = userTecnico
            caso.casEstado = "En Proceso"
            caso.save()
            # enviar correo al técnico
            asunto = 'Asignación Caso - Mesa de Servicio - CTPI-CAUCA'
            mensajeCorreo = f'Cordial saludo, <b>{userTecnico.first_name} {userTecnico.last_name}</b>, nos permitimos \
                    informarle que se le ha asignado un caso para dar solución. Código de Caso:  \
                    <b>{caso.casCodigo}</b>. <br><br> Se solicita se atienda de manera oportuna \
                    según los acuerdos de solución establecidos para la Mesa de Servicios del CTPI-CAUCA.\
                    <br><br>Lo invitamos a ingresar al sistema para gestionar sus casos asignados en la siguiente url:\
                    http://mesadeservicioctpicauca.sena.edu.co.'
            thread = threading.Thread(
                target=enviarCorreo, args=(asunto, mensajeCorreo, [userTecnico.email]))
            thread.start()
            mensaje = "Caso asignado"
        except Error as error:
            mensaje = str(error)
        return redirect('/listarCasosParaAsignar/')
    else:
        mensaje = "Debe primero iniciar sesión"
        return render(request, "login.html", {"mensaje": mensaje})


def listarCasosTecnicos (request):
    if request.user.is_authenticated:
        try:
            ListaCasos = Caso.objects.filter(cas_estado="En Proceso", cas_usuario=request.user)
            listaTipoProcedimientos=TipoProcedimiento.objects.all().values()
            mensaje = "Listado de casos asignados"
        except Error as error:
            mensaje=str(error)
        retorno = {"mensaje":mensaje, "ListaCasos":ListaCasos,"listaTipoSolucion":tipoSolucion,"listaTipoProcedimientos":listaTipoProcedimientos}
        return render(request, "tecnico/listaCasosAsignados.html", retorno)
    
    else:
        mensaje="Debes iniciar sesion"
        return render (request,"login.html",{"mensaje":mensaje})

def solucionCaso(request):
    if request.user.is_authenticated:
        procedimiento=request.POST['txtProcedimiento']
        tipoProc=int(request.POST['cbTipoProcedimiento'])
        tipoProcedimiento=TipoProcedimiento.object.get(pk=tipoProc)
        TipoSolucion=request.POST['cbTipoSolicion']
        idCaso=int(request.POST['idCaso'])
        caso=Caso.objects.get(pk=idCaso)
        solucionCaso=SolucionCaso(solCaso=caso,
                                  solProcedimiento=procedimiento,
                                  solTipoSolucion=tipoSolucion)
        solucionCaso.save()
        
        if(tipoSolucion== "Definitiva"):
            caso.casEstado ="Finalizada"
            caso.save()
            
        SolucionCasoTipoProcedimientos=SolucionCasoTipoProcedimientos(
            solSolucionCaso=solucionCaso,
            solTipoProcedimiento=tipoProcedimiento
        )
        SolucionCasoTipoProcedimientos.save()
    else:
        mensaje='Debe iniciar secion'
        return render(request, "login.html",{"mensaje":mensaje})
    
    
def salir(request):
    auth.logout(request)
    return render(request,"login.html",{"mensaje":"Salio de sesion"})
   
    