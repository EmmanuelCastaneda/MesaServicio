# Generated by Django 5.0.6 on 2024-05-20 13:16

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='OficinaAmbiente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ofiTipo', models.CharField(choices=[('Administrativo', 'Administrativo'), ('Formacion', 'Formacion')], db_comment='Tipo Ambiente', max_length=15)),
                ('ofiNombre', models.CharField(db_comment='Nombre Ambiente', max_length=50, unique=True)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y Hora de Creacion')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora ultima actualizacion')),
            ],
        ),
        migrations.CreateModel(
            name='TipoProcedimiento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipNombre', models.CharField(db_comment='Nombre del tipo de procedimiento', max_length=20, unique=True)),
                ('tipDescripcion', models.TextField(db_comment='Texto con la descripcion del procedimiento', max_length=1000)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y Hora de Creacion')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora ultima actualizacion')),
            ],
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solDescripcion', models.TextField(db_comment='Texto que describe las solicitudes del empleado', max_length=1000)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y Hora de Creacion')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora ultima actualizacion')),
                ('solOficinaAmbiente', models.ForeignKey(db_comment='Hace referencia al ambiento o lugar donde se encuentra el equipo', on_delete=django.db.models.deletion.PROTECT, to='MesaAyuda.oficinaambiente')),
            ],
        ),
        migrations.CreateModel(
            name='Caso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('casCodigo', models.CharField(db_comment='Codigo del caso', max_length=10, unique=True)),
                ('casEstado', models.CharField(choices=[('Solicitada', 'Solicitada'), ('En Proceso', 'En proceso'), ('Finalizada', 'Finalizada')], db_comment='Estado del caso', max_length=15)),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora ultima actualizacion')),
                ('casSolicitud', models.ForeignKey(db_comment='Hace Referencia a lasolicitud que genero el empleado', on_delete=django.db.models.deletion.PROTECT, to='MesaAyuda.solicitud')),
            ],
        ),
        migrations.CreateModel(
            name='SolucionCaso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solProcedimiento', models.TextField(db_comment='Texto del procedimiento realizado en la solución del caso', max_length=2000)),
                ('solTipoSolucion', models.CharField(choices=[('Parcial', 'Parcial'), ('Definitiva', 'Definitiva')], db_comment='Tipo de la solucuín, si es parcial o definitiva', max_length=20)),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y hora del registro')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora última actualización')),
                ('solCaso', models.ForeignKey(db_comment='Hace referencia al caso que genera la solución', on_delete=django.db.models.deletion.PROTECT, to='MesaAyuda.caso')),
            ],
        ),
        migrations.CreateModel(
            name='SolucionCasoTipoProcedimientos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solSolucionCaso', models.ForeignKey(db_comment='Hace referencia a la solución del Caso', on_delete=django.db.models.deletion.PROTECT, to='MesaAyuda.solucioncaso')),
                ('solTipoProcedimiento', models.ForeignKey(db_comment='Hace referencia al tipo de procedimiento de la solución', on_delete=django.db.models.deletion.PROTECT, to='MesaAyuda.tipoprocedimiento')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('userTipo', models.CharField(choices=[('Administrativo', 'Administrativo'), ('Instructor', 'Instructor')], db_comment='Tipo usuario', max_length=15)),
                ('userFoto', models.ImageField(blank=True, db_comment='Foto del Usuario', null=True, upload_to='foto')),
                ('fechaHoraCreacion', models.DateTimeField(auto_now_add=True, db_comment='Fecha y Hora de Creacion')),
                ('fechaHoraActualizacion', models.DateTimeField(auto_now=True, db_comment='Fecha y hora ultima actualizacion')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='solicitud',
            name='solUsuario',
            field=models.ForeignKey(db_comment='Hace referencia al empleado que hace la solicitud', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='caso',
            name='casUsuario',
            field=models.ForeignKey(db_comment='Empleado de soporte tecnico asignado al caso', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
