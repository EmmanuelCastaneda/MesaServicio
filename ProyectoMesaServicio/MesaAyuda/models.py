from django.db import models
from django.contrib.auth.models import AbstractUser

tipoOficinaAmbiente=[
    ('Administrativo','Administrativo'),
    ('Formacion','Formacion')
]
tipoEmpleado=[
    ('Administrativo','Administrativo'),
    ('Instructor','Instructor')
]
tipoUsuario=[
    ('Administrativo','Administrativo'),
    ('Instructor','Instructor'),
    ('Tecnico','Tecnico'),
]
estadoCaso=[
    ('Solicitada','Solicitada'),
    ('En Proceso','En proceso'),
    ('Finalizada','Finalizada')
]
tipoSolucion = [
    ('Parcial', 'Parcial'),
    ('Definitiva', 'Definitiva')
]

class OficinaAmbiente(models.Model):
    ofiTipo=models.CharField(max_length=15,choices=tipoOficinaAmbiente,db_comment='Tipo Ambiente')
    ofiNombre=models.CharField(max_length=50,unique=True,db_comment='Nombre Ambiente')
    fechaHoraCreacion=models.DateTimeField(auto_now_add=True,
                                           db_comment='Fecha y Hora de Creacion')
    fechaHoraActualizacion=models.DateTimeField(auto_now=True,db_comment='Fecha y hora ultima actualizacion')
    
    def __str__(self)->str:
        return self.ofiNombre
    
class User(AbstractUser):
    userTipo=models.CharField(max_length=15, choices=tipoUsuario,db_comment='Tipo usuario')
    userFoto=models.ImageField(
        upload_to=f"foto",null=True,blank=True,db_comment='Foto del Usuario')
    fechaHoraCreacion=models.DateTimeField(auto_now_add=True,
                                           db_comment='Fecha y Hora de Creacion')
    fechaHoraActualizacion=models.DateTimeField(auto_now=True,db_comment='Fecha y hora ultima actualizacion')
    
    def __str__(self)->str:
        return self.username
    
class Solicitud(models.Model):
    solUsuario=models.ForeignKey(User,on_delete=models.PROTECT,
                                 db_comment='Hace referencia al empleado que hace la solicitud')
    solDescripcion=models.TextField(max_length=1000,
                                    db_comment='Texto que describe las solicitudes del empleado')
    solOficinaAmbiente=models.ForeignKey(
        OficinaAmbiente,on_delete=models.PROTECT,db_comment='Hace referencia al ambiento o lugar donde se encuentra el equipo')
    fechaHoraCreacion=models.DateTimeField(auto_now_add=True,
                                           db_comment='Fecha y Hora de Creacion')
    fechaHoraActualizacion=models.DateTimeField(auto_now=True,db_comment='Fecha y hora ultima actualizacion')
    
    def __str__(self) -> str:
        return self.solDescripcion
    
class Caso(models.Model):
    casSolicitud=models.ForeignKey(Solicitud,on_delete=models.PROTECT,
                                   db_comment='Hace Referencia a lasolicitud que genero el empleado')
    casCodigo=models.CharField(max_length=20,unique=True,
                               db_comment='Codigo del caso')
    casUsuario=models.ForeignKey(User,on_delete=models.PROTECT,
                                 db_comment='Empleado de soporte tecnico asignado al caso')
    casEstado=models.CharField(max_length=15,choices=estadoCaso,db_comment='Estado del caso')
    
    fechaHoraActualizacion=models.DateTimeField(auto_now=True,
                                                db_comment='Fecha y hora ultima actualizacion')
    
    def __str__(self) -> str:
        return self.casCodigo
    
class TipoProcedimiento(models.Model):
    tipNombre=models.CharField(max_length=20,unique=True,db_comment='Nombre del tipo de procedimiento')
    
    tipDescripcion=models.TextField(max_length=1000,db_comment="Texto con la descripcion del procedimiento")
    
    fechaHoraCreacion=models.DateTimeField(auto_now_add=True,
                                           db_comment='Fecha y Hora de Creacion')
    fechaHoraActualizacion=models.DateTimeField(auto_now=True,db_comment='Fecha y hora ultima actualizacion')
    
    def __str__(self) -> str:
        return self.tipNombre
    
class SolucionCaso(models.Model):
    solCaso = models.ForeignKey(Caso, on_delete=models.PROTECT,
                                db_comment="Hace referencia al caso que genera la solución")
    solProcedimiento = models.TextField(max_length=2000,
                                        db_comment="Texto del procedimiento realizado en la solución del caso")
    solTipoSolucion = models.CharField(max_length=20, choices=tipoSolucion,
                                       db_comment="Tipo de la solucuín, si es parcial o definitiva")
    fechaHoraCreacion = models.DateTimeField(auto_now_add=True,
                                             db_comment="Fecha y hora del registro")
    fechaHoraActualizacion = models.DateTimeField(auto_now=True,
                                                  db_comment="Fecha y hora última actualización")
    
    def __str__(self) -> str:
        return self.solTipoSolucion
    
class SolucionCasoTipoProcedimientos(models.Model):
    solSolucionCaso = models.ForeignKey(SolucionCaso, on_delete=models.PROTECT,
                                        db_comment="Hace referencia a la solución del Caso")
    solTipoProcedimiento = models.ForeignKey(TipoProcedimiento, on_delete=models.PROTECT,
                                             db_comment="Hace referencia al tipo de procedimiento de la solución")
    
    def __str__(self) -> str:
        return self.solTipoProcedimiento
    
# class SolucionCaso(models.Model):
#    solCaso=models.ForeignKey(Caso,on_delete=models.PROTECT,db_comment='Hace referencia al caso que genera la solicitud')
   
#    solProcedimiento=models.TextField(max_length=2000,
#                                      db_comment='Texto que describe el procedimiento para solucionar el caso')
#    solTi
    

    

# class Empleados(models.Model):
#     empNombre=models.CharField(max_length=50,db_comment='Nombre Empleado'),
#     empApellidos=models.CharField(max_length=50,db_comment='Apellidos empleado'),
#     empCorreo=models.CharField(max_length=50,unique=True,db_comment='Correo empleado'),
#     empTipo=models.CharField(max_length=50,choices=tipoEmpleado,db_comment='Tipo Empelado'),
    
# class Roles(models.Model):
#     rolNombre=models.CharField(max_length=50,db_comment='Nombre Rol'),






# BASE DE DATOS PROYECTO

# tipoDocumento=[
#     ('Tarjeta de Identidad','Tarjeta de Identidad'),
#     ('Cedula','Cedula'),
#     ('Cedula Extranjera','Cedula Extranjera'),
#     ('PEP','PEP'),
#     ('Permiso Por Proteccion Temporal','Permiso Por Proteccion Temporal')
# ]
# tipoRol=[
#     ('Administrador','Administrador'),
#     ('Guardia','Guardia'),
#     ('Aprendiz','Aprendiz'),
#     ('Instructor','Instructor')
# ]
# jornadaFicha=[
#     ('Diurna','Diurna'),
#     ('Tarde','Tarde'),
#     ('Nocturna','Nocturna'),
# ]
# tipoFormacion=[
#     ('Formacion Basica','Formacion Basica'),
#     ('Tecnologo','Tecnologo'),
#     ('Tecnico','Tecnico'),
# ]

# class contactEmergencia(models.Model):
#     apellido_cntEmerg=models.CharField(max_length=50)
#     celular_cntEmerg=models.CharField(max_length=12)
#     nombre_cntEmerg=models.CharField(max_length=50)
#     relacion_cntEmerg=models.CharField(max_length=30)
    
# class programa(models.Model):
#     codigo_programa=models.CharField(max_length=20,unique=True)
#     nombre_programa=models.CharField(max_length=100)

# class objetos(models.Model):
#     marca_objeto=models.CharField(max_length=20)
#     modelo_objeto=models.CharField(max_length=20,unique=True)
#     descripcion_objeto=models.TextField(max_length=1000,db_comment="Texto con la descripcion ")
#     foto_objeto=models.ImageField(
#         upload_to=f"foto",null=True,blank=True,db_comment='Foto del Objeto')

# class rol (models.Model):
#     nombre_rol=models.CharField(max_length=20, choices=tipoRol,
#                                        db_comment="Tipo de rol")
    
#     # deberia ser tipo rol
    
# class registro_facial (models.Model):
#     datos_biometricos_registro= models.Model(max_length=50)
#     #Pasar datos_biometricos_registro para agregarlo en un FILE
#     fecha_registro=models.DateTimeField(auto_now_add=True,
#                                              db_comment="Fecha y hora del registro")

# # class tipoDocumentos (models.Model):
# #     nombre_documento=models.CharField(max_length=50, choices=tipoDocumento,
# #                                        db_comment="Tipo de documento")
# #     # deberia ser tipo de documento
    
    
# class ficha (models.Model):
#     numero_ficha=models.CharField(max_length=20,unique=True)
#     aprendices_matriculado_ficha=models.IntegerField()
#     aprendices_actuales_ficha=models.IntegerField()
#     jornada_ficha=models.CharField(max_length=50, choices=jornadaFicha,
#                                        db_comment="Tipo de jornada")
#     tipo_formacion_ficha=models.CharField(max_length=30,choices=tipoFormacion,
#                                           db_comment="Tipo de Formacion")
#     programa=models.ForeignKey(programa, on_delete=models.PROTECT,
#                                              db_comment="Hace referencia al Programa de Formacion")
    

    
# class usuarios(models.Model):
#     nombre_usuario=models.CharField(max_length=50)
#     apellido_usuario=models.CharField(max_length=50)
#     genero_usuario=models.CharField(max_length=20)  
#     correo_usuario=models.CharField(max_length=50) 
#     numero_documento_usuario=models.CharField(max_length=20)
#     tipo_documento=models.CharField(max_length=50, choices=tipoDocumento,
#                                        db_comment="Tipo de documento")
#     objetos=models.ForeignKey(objetos, on_delete=models.PROTECT,
#                                              db_comment="Hace referencia al los objetos registrados del usuario ")
#     registro_facial=models.ForeignKey(registro_facial, on_delete=models.PROTECT,
#                                              db_comment="Hace referencia al registro facial del usuario")
#     contacto_emergencia=models.ForeignKey(contactEmergencia, on_delete=models.PROTECT,
#                                              db_comment="Hace referencia al contacto de emergencia del usuario")
#     rol=models.ForeignKey(rol,on_delete=models.PROTECT,
#                           db_comment="Hace referencia al rol del usuario")
#     ficha=models.ForeignKey(ficha,on_delete=models.PROTECT,
#                           db_comment="Hace referencia a la ficha del usuario")


# class reconocimiento_facial(models.Model):
#     codigo_recono=models.CharField(max_length=20,unique=True)
#     fecha_entrada_recono=models.DateTimeField(auto_now_add=True,
#                                              db_comment="Fecha y hora de entrada")
#     fecha_salida_recono=models.DateTimeField(auto_now_add=True,
#                                              db_comment="Fecha y hora de salida")
#     usuario_recono=models.ForeignKey(usuarios, on_delete=models.PROTECT,
#                                              db_comment="Hace referencia al Usuario que reconoce ")